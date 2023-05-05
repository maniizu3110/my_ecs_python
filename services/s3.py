from aws_cdk import (
    aws_s3 as s3,
    Stack
)

from services.config.config import Config


class S3Buckets:
    def __init__(self, stack: Stack, config: Config):
        for name in config.s3_bucket_names:
            s3.Bucket(stack, name, bucket_name=name, versioned=True,
                      encryption=s3.BucketEncryption.S3_MANAGED)
