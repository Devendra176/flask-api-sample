import boto3
import os
from datetime import datetime

from flask import current_app


class s3Operations:
    def __init__(self):
        self.bucket = current_app.config["S3_BUCKET"]
        self.aws_access_key_id = current_app.config['S3_KEY']
        self.aws_secret_access_key = current_app.config['S3_SECRET']
        self.s3_client = boto3.client(
                        "s3",
                        aws_access_key_id = self.aws_access_key_id,
                        aws_secret_access_key = self.aws_secret_access_key,
                        )
        self.s3_resource = boto3.resource(
                        's3',
                        aws_access_key_id = self.aws_access_key_id,
                        aws_secret_access_key = self.aws_secret_access_key,
                        )
    def send_file_s3(self,file_path,aws_file_name):
        """
        This method is used to send images into s3 bucket.
        """
        output = self.s3_client.upload_file(file_path, self.bucket, aws_file_name)
        return output

    def get_file_from_s3(self):
        s3 = self.s3_resource
        items = []
        for bucket in s3.buckets.all():
            items = [item.key for item in bucket.objects.all()]

        res = [tuple(j.split('/')) for j in items]
        itme_dict= {}
        for key,value in res:
            itme_dict.setdefault(key, []).append(value)

        return itme_dict





def rename_file(filename):
    """
    This method is used to rename the images.
    We are using timestap for file name.
    """
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    timestamp = str(timestamp)
    file ,extension = os.path.splitext(filename)
    new_name = "".join([timestamp,extension])
    return new_name

