# upload_to_s3.py
import boto3
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Load AWS credentials
load_dotenv()
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Set up S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

def upload_to_s3(local_file_path, source_name):
    bucket_name = 'octabyte-data-pipeline'  
    today_str = datetime.now().strftime('%Y-%m-%d')
    s3_key = f'raw/{source_name}/{today_str}/{os.path.basename(local_file_path)}'

    try:
        s3.upload_file(local_file_path, bucket_name, s3_key)
        print(f"Uploaded to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Upload failed: {e}")

# Usage: python upload_to_s3.py leadiq_2025-07-07.json leadiq
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python upload_to_s3.py <filename.json> <source_name>")
    else:
        upload_to_s3(sys.argv[1], sys.argv[2])
