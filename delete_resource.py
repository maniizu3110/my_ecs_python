from setup import env
import boto3


def delete_ecr_repository():
    ecr_client = boto3.client(
        'ecr',
        region_name=env.aws_region
    )
    ecr_client.delete_repository(
        repositoryName=env.default_service_name,
        force=True
    )
    print(f"Deleted ECR repository: {env.default_service_name}")


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
    delete_ecr_repository()
    delete_s3_bucket(env.default_service_name)
    delete_s3_bucket(env.default_service_name+"-backstage")


if __name__ == "__main__":
    main()
