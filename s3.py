import os

import boto3
# import json

# bucket = 'data-brains-bucket'
# prefix = "hh.ru/"
# yandex_profile = 'default'
# link_to_file = '123/ReadME.md'
#
# session = boto3.session.Session()
#
# s3 = session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net')
#
# s3.upload_file('ReadME.md', bucket, link_to_file)
#
# get_object_response = s3.get_object(Bucket=bucket, Key=link_to_file)
# file = get_object_response['Body'].read().decode('utf-8')
# print(file)


class S3:
    bucket = 'data-brains-bucket'
    prefix = "hh.ru/"
    profile = 'default'

    @staticmethod
    def upload(host_path, s3_path):
        session = boto3.session.Session()
        s3 = session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net')
        s3.upload_file(host_path, S3.bucket, S3.prefix + s3_path)
        os.remove(host_path)
