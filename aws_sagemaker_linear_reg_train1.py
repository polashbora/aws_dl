import numpy as np
import boto3
import sagemaker
import io
import sagemaker.amazon.common as smac
import pandas as pd

dataset = pd.read_csv("well_log_train.csv")

feature_dataset = dataset[['Density', 'Sonic' ]]
features = np.array(feature_dataset.values).astype('float32')


label_dataset= dataset[['Gamma']]
labels = np.array(label_dataset.values).astype('float32')
labels_vec = np.squeeze(np.asarray(labels))


buffer = io.BytesIO()
smac.write_numpy_to_dense_tensor(buffer, features, labels_vec)
buffer.seek(0)
bucket='forecastdemopolashbora'
key = 'linearregression'
boto3.resource('s3').Bucket(bucket).Object(key).upload_fileobj(buffer)
s3_training_data_location = 's3://{}/{}'.format(bucket, key)
output_location='s3://{}/'.format(bucket)
from sagemaker.amazon.amazon_estimator import get_image_uri
linear_container = get_image_uri(boto3.Session().region_name, 'linear-learner')

role = 'sagemaker_full_role'

sagemaker_session = sagemaker.Session()

linear = sagemaker.estimator.Estimator(linear_container,
                                       role=role,
                                       train_instance_count=1,
                                       train_instance_type='ml.c4.2xlarge',
                                       output_path=output_location,
                                       sagemaker_session=sagemaker_session)


linear.set_hyperparameters(feature_dim=2,
                           num_models=20,
                           predictor_type='regressor')


linear.fit({'train': s3_training_data_location})

linear_predictor = linear.deploy(initial_instance_count=1,
                                 instance_type='ml.c4.2xlarge',
                                 endpoint_name='polash-sagemaker-regression-v4')
from sagemaker.predictor import csv_serializer, json_deserializer

linear_predictor.content_type = 'text/csv'
linear_predictor.serializer = csv_serializer
linear_predictor.deserializer = json_deserializer

test_dataset = pd.read_csv("well_log_test_short.csv")
test_feature_dataset = test_dataset[['Density', 'Sonic']]

test_features = np.array(test_feature_dataset.values).astype('float32')


prediction = linear_predictor.predict(test_features)

mylist=[]
for a in (prediction['predictions']):
    mylist.append(a['score'])

mydf=pd.DataFrame(mylist,columns=['Comp_Gamma'])
df_col = pd.concat([test_dataset,mydf], axis=1)
print(df_col)
