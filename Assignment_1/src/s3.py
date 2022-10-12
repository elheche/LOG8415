import json
import shutil

from mypy_boto3_s3 import S3Client


def create_bucket(s3: S3Client, bucket: str) -> None:
    try:
        print('Creating a S3 bucket...')
        s3.create_bucket(Bucket=bucket)
    except Exception as e:
        print(e)
    else:
        print(f'S3 bucket created successfully.\n{bucket}')


def put_bucket_policy(s3: S3Client, s3_config: dict, aws_user_account: str, role_arn) -> None:
    bucket_policy = s3_config['BucketPolicy']
    bucket_policy['Statement'][0]['Principal'] = {"AWS": [aws_user_account]}
    bucket_policy['Statement'][1]['Principal'] = {"AWS": [role_arn]}
    try:
        print('Applying a policy to an S3 Bucket...')
        s3.put_bucket_policy(
            Bucket=s3_config['Bucket'],
            Policy=json.dumps(bucket_policy)
        )
    except Exception as e:
        print(e)
    else:
        print(f'Policy successfully applied to bucket {s3_config["Bucket"]}')


def upload_server_app_to_s3_bucket(s3: S3Client, bucket: str) -> None:
    try:
        print('Uploading a server app to an S3 Bucket...')
        shutil.make_archive('server', 'zip', './server')
        s3.upload_file('./server.zip', bucket, 'server.zip')
    except Exception as e:
        print(e)
    else:
        print(f'Server app successfully uploaded to bucket {bucket}')
