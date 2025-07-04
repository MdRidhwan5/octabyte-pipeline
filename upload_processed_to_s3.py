from dotenv import load_dotenv
import os
import boto3

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

file_name = 'thelogisticsoflogistics_2025-07-04.json'
bucket_name = 'octabyte-data-pipeline'
s3_path = 'raw/logisticsoflogistics/2025-07-04/' + file_name

try:
    s3.upload_file(file_name, bucket_name, s3_path)
    print(f"Uploaded {file_name} to s3://{bucket_name}/{s3_path}")
except Exception as e:
    print(f"Upload failed: {e}")
