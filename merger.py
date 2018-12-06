import os
from boto3.session import Session
import boto3
from mailmerge import MailMerge
from logger import Logger

LOG = Logger()

AWS_ACCESSKEY_ID = os.environ.get('AWS_ACCESSKEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

session = Session(aws_access_key_id=AWS_ACCESSKEY_ID,
                  aws_secret_access_key=AWS_SECRET_KEY)


def merge(data, template, template_bucket_name, output_bucket_name, user):
    s3_res = session.resource('s3')
    s3 = boto3.client('s3')
    bucket = s3_res.Bucket(template_bucket_name)
    # Download template from S3, save in /tmp
    bucket.download_file(template, '/tmp/temp.docx')

    document = MailMerge('/tmp/temp.docx')
    # LOG.console(document.get_merge_fields())
    document.merge_pages([data])
    document.write('/tmp/output.docx')

    key_file_name = "{0}/output.docx".format(user)
    data = open('/tmp/output.docx', 'rb')
    s3_res.Bucket(output_bucket_name).put_object(Key=key_file_name, Body=data)
    
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': output_bucket_name,
            'Key': key_file_name
        }
    )
    return url
