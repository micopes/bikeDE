import logging
import boto3
from botocore.exceptions import ClientError
import os

from keys import ACCESS_KEY, SECRET_ACCESS_KEY

class S3Operator:
    def upload_file_s3(self, bucket, df, file_name):
        s3 = boto3.client('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_ACCESS_KEY)
        encode_file = df.to_parquet()

        try:
            s3.put_object(Bucket = bucket, Key = file_name, Body = encode_file)
            return True
        except:
            return False
