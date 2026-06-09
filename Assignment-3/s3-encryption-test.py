import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):

    buckets = s3.list_buckets()

    unencrypted_buckets = []

    for bucket in buckets['Buckets']:

        bucket_name = bucket['Name']

        try:
            s3.get_bucket_encryption(
                Bucket=bucket_name
            )

            print(f"{bucket_name} : Encryption Enabled")

        except ClientError as e:

            error_code = e.response['Error']['Code']

            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':

                print(f"{bucket_name} : Encryption NOT Enabled")

                unencrypted_buckets.append(bucket_name)

    return {
        'statusCode': 200,
        'unencrypted_buckets': unencrypted_buckets
    }