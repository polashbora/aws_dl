import boto3
import datetime

session = boto3.Session()
s3_client = session.client("s3")


now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))

try:


   print("Uploading file")

   tc = boto3.s3.transfer.TransferConfig(multipart_threshold=1024 * 25, max_concurrency=20, use_threads=True)
   t = boto3.s3.transfer.S3Transfer(client=s3_client, config=tc)
   t.upload_file("F3_Demo_2016_training_v6.zip", "forecastdemopolashbora", "F3_Demo_2016_training_v6_multipart1.zip")

except Exception as e:
   print("Error uploading: {}".format(e))


now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
