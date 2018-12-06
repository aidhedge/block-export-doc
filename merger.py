import os
from boto3.session import Session
import boto3
from mailmerge import MailMerge

AWS_ACCESSKEY_ID = os.environ.get('AWS_ACCESSKEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

session = Session(aws_access_key_id=AWS_ACCESSKEY_ID,
                  aws_secret_access_key=AWS_SECRET_KEY)


def merge(data, template, bucket_name, user):
    s3_res = session.resource('s3')
    s3 = boto3.client('s3')
    bucket = s3_res.Bucket(bucket_name)
    bucket.download_file(template, './temp-storage/temp.docx')

    document = MailMerge('./temp-storage/temp.docx')
    document.write('./temp-storage/output.docx')

    key_file_name = "{0}/output.docx".format(user)
    data = open('./temp-storage/output.docx', 'rb')
    s3_res.Bucket(bucket_name).put_object(Key=key_file_name, Body=data)
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': key_file_name
        }
    )
    return url
