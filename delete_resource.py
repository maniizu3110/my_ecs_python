from services.utils.convert_build_path_to_s3 import convert_to_s3_object_name
from services.utils.get_repository_name import get_repository_name
from setup import BUCKET_PREFIX, env
import boto3


def delete_ecr_repository(repository):
    ecr_client = boto3.client(
        'ecr',
        region_name=env.aws_region
    )
    ecr_client.delete_repository(
        repositoryName=repository,
        force=True
    )
    print(f"Deleted ECR repository: {repository}")


def delete_s3_bucket(bucket_name):
    s3_client = boto3.client(
        's3',
        region_name=env.aws_region
    )

    bucket = boto3.resource('s3').Bucket(bucket_name)
    bucket.object_versions.delete()

    s3_client.delete_bucket(
        Bucket=bucket_name
    )
    print(f"Deleted S3 bucket: {bucket_name}")


def main():
    repository = f"{env.default_service_name}-{get_repository_name(env.github_repository_url)}-{convert_to_s3_object_name(env.build_path)}"
    bucket_name = f"{BUCKET_PREFIX}-{env.default_service_name}"
    delete_ecr_repository(repository)
    delete_s3_bucket(bucket_name)
    delete_s3_bucket(bucket_name+"-backstage")


if __name__ == "__main__":
    main()
