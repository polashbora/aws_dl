import boto3
import time
import subprocess
import pandas as pd
import json

session = boto3.Session(region_name='ap-south-1')
forecast = session.client(service_name='forecast')
forecastquery = session.client(service_name='forecastquery')
df = pd.read_csv("item-demand-time.csv", dtype = object, names=['timestamp','value','item'])
print(df.head(3))

s3 = session.client('s3')

key="item-demand-time.csv"

bucket_name="forecastdemopolashbora"
###s3.upload_file(Filename="item-demand-time.csv", Bucket="forecastdemopolashbora", Key=key)


jan_to_oct = df[(df['timestamp'] >= '2014-01-01') & (df['timestamp'] <= '2014-10-31')]

# Select the month of December for another dataframe.
df = pd.read_csv("item-demand-time.csv", dtype = object, names=['timestamp','value','item'])
remaining_df = df[(df['timestamp'] >= '2014-10-31') & (df['timestamp'] <= '2014-12-01')]

jan_to_oct.to_csv("item-demand-time-train.csv", header=False, index=False)
remaining_df.to_csv("item-demand-time-validation.csv", header=False, index=False)

key="elec_data/item-demand-time-train.csv"

boto3.Session().resource('s3').Bucket(bucket_name).Object(key).upload_file("item-demand-time-train.csv")

DATASET_FREQUENCY = "H"
TIMESTAMP_FORMAT = "yyyy-MM-dd hh:mm:ss"
project = 'util_power_forecastdemo'
datasetName= project+'_ds'
datasetGroupName= project +'_dsg'
s3DataPath = "s3://"+bucket_name+"/"+key


create_dataset_group_response = forecast.create_dataset_group(DatasetGroupName=datasetGroupName, Domain="CUSTOM",)
datasetGroupArn = create_dataset_group_response['DatasetGroupArn']
print(datasetGroupArn)
#datasetGroupArn="arn:aws:forecast:ap-south-1:946837915266:dataset-group/util_power_forecastdemo_dsg"


# Specify the schema of your dataset here. Make sure the order of columns matches the raw data files.
schema ={
   "Attributes":[
      {
         "AttributeName":"timestamp",
         "AttributeType":"timestamp"
      },
      {
         "AttributeName":"target_value",
         "AttributeType":"float"
      },
      {
         "AttributeName":"item_id",
         "AttributeType":"string"
      }
   ]
}

response=forecast.create_dataset(
                    Domain="CUSTOM",
                    DatasetType='TARGET_TIME_SERIES',
                    DatasetName=datasetName,
                    DataFrequency=DATASET_FREQUENCY,
                    Schema = schema
    )
datasetArn = response['DatasetArn']
#datasetArn="arn:aws:forecast:ap-south-1:946837915266:dataset/util_power_forecastdemo_ds"

print(forecast.describe_dataset(DatasetArn=datasetArn))
forecast.update_dataset_group(DatasetGroupArn=datasetGroupArn, DatasetArns=[datasetArn])
iam = boto3.client("iam")

role_name = "ForecastRoleDemo"
assume_role_policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "forecast.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

try:
    create_role_response = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy_document)
    )
    role_arn = create_role_response["Role"]["Arn"]
except iam.exceptions.EntityAlreadyExistsException:
    print("The role " + role_name + " exists, ignore to create it")
    role_arn = boto3.resource('iam').Role(role_name).arn

# Attaching AmazonForecastFullAccess to access all actions for Amazon Forecast
policy_arn = "arn:aws:iam::aws:policy/AmazonForecastFullAccess"
iam.attach_role_policy(
    RoleName=role_name,
    PolicyArn=policy_arn
)

# Now add S3 support
iam.attach_role_policy(
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess',
    RoleName=role_name
)
time.sleep(60)  # wait for a minute to allow IAM role policy attachment to propagate

print(role_arn)

datasetImportJobName = 'EP_DSIMPORT_JOB_TARGET'
ds_import_job_response=forecast.create_dataset_import_job(DatasetImportJobName=datasetImportJobName,
                                                          DatasetArn=datasetArn,
                                                          DataSource= {
                                                              "S3Config" : {
                                                                 "Path":s3DataPath,
                                                                 "RoleArn": role_arn
                                                              }
                                                          },
                                                          TimestampFormat=TIMESTAMP_FORMAT
                                                         )


ds_import_job_arn=ds_import_job_response['DatasetImportJobArn']
print(ds_import_job_arn)

print(forecast.describe_dataset_import_job(DatasetImportJobArn=ds_import_job_arn))