from services.config.config import Config
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds
from services.config.ecs_service import ECSService
from services.config.rds import RDSConfig
from services.config.env import Env
import os
import boto3
from services.utils.find_available_cidr import find_available_cidr_block
from services.utils.get_domain_detail import get_domain_and_subdomain
from services.utils.get_ecs_services_env import get_file_content, list_env_file_names_with_prefix, list_env_files
from services.utils.load_script_from_env import load_pre_build_script

BUCKET_PREFIX = "eighty-and-co"


def remove_env_suffix(env_file_name):
    return env_file_name.replace(".env", "")


def get_env_content_as_dict(bucket_name, env_file_name):
    env_content = get_file_content(bucket_name, env_file_name)
    env_content_as_dict = {}
    for line in env_content.splitlines():
        if "=" in line:
            # Split only once, in case value contains "="
            key, value = line.split("=", 1)
            env_content_as_dict[key] = value
    return env_content_as_dict


def create_ecs_cluster_services():
    env_bucket_name = f"{BUCKET_PREFIX}-{env.default_service_name}-backstage"
    env_file_names = list_env_files(env_bucket_name)
    ecs_cluster_services = []
    for env_file_name in env_file_names:
        ecr_name = f"{env.env}-{remove_env_suffix(env_file_name)}"
        image_url = get_latest_ecr_image_url(ecr_name)
        env_dict = get_env_content_as_dict(env_bucket_name, env_file_name)
        subdomain = get_domain_and_subdomain(env_dict['DOMAIN'])[
            'subdomain'] if "DOMAIN" in env_dict else None
        if image_url:
            ecs_cluster_services.append(
                ECSService(
                    name=ecr_name,
                    image_url=image_url,
                    domain_prefix=subdomain,
                    container_port=env_dict['PORT'],
                    desired_count=1,
                    health_check_path=env_dict['HEALTH_CHECK_PATH'],
                    healthy_http_codes=env_dict['HEALTH_CHECK_CODES'],
                    cpu=256,
                    memory_limit_mib=512,
                )
            )
    return ecs_cluster_services


def get_latest_ecr_image_url(repository_name: str) -> str:
    ecr_client = boto3.client('ecr')
    try:
        response = ecr_client.describe_images(repositoryName=repository_name)
        if len(response['imageDetails']) > 0:
            latest_image = sorted(
                response['imageDetails'], key=lambda x: x['imagePushedAt'], reverse=True)[0]
            registry_id = latest_image['registryId']
            region = env.aws_region
            return f"{registry_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{latest_image['imageTags'][0]}"
        else:
            return ""
    except ecr_client.exceptions.RepositoryNotFoundException:
        return ""


env = Env(
    # 　Values for which no default is set are assumed to be taken from .env
    service_name=os.getenv("SERVICE_NAME"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_region=os.getenv("AWS_REGION"),
    env=os.getenv("ENV"),
    github_repository_url=os.getenv("GITHUB_REPOSITORY_URL"),
    port=int(os.getenv("PORT")),
    build_path=os.getenv("BUILD_PATH"),
    dockerfile_name=os.getenv("DOCKERFILE_NAME"),
    domain=os.getenv("DOMAIN"),
    database_kind=os.getenv("DATABASE_KIND", "mysql"),
    vpc_cidr=os.getenv("VPC_CIDR", find_available_cidr_block()),
    pre_build_script=load_pre_build_script(".env"),
    health_check_path=os.getenv("HEALTH_CHECK_PATH", "/"),
    health_check_codes=os.getenv("HEALTH_CHECK_CODES", "200-499"),

    rds_allocated_storage=int(os.getenv("RDS_ALLOCATED_STORAGE", 20)),
    rds_instance_type=os.getenv("RDS_INSTANCE_TYPE", "t3.micro"),
    rds_deletion_protection=os.getenv("RDS_DELETION_PROTECTION", False),
    rds_publicly_accessible=os.getenv("RDS_PUBLICLY_ACCESSIBLE", True),
)


config = Config(
    env=env.env,
    cdk_env={
        'account': os.getenv("CDK_DEFAULT_ACCOUNT"),
        'region': os.getenv("AWS_REGION")
    },
    domain=env.domain,
    default_service_name=env.default_service_name,
    pascal_service_name=env.pascal_service_name,
    ecr_repository_names=list_env_file_names_with_prefix(
        f"{BUCKET_PREFIX}-{env.default_service_name}", env.env),
    s3_bucket_names=[],
    vpc_cidr=env.vpc_cidr,
    rds_config=RDSConfig(
        database_name=env.default_service_name,
        kind=env.database_kind,
        allocated_storage=env.rds_allocated_storage,
        instance_type=ec2.InstanceType(env.rds_instance_type),
        deletion_protection=env.rds_deletion_protection,
        publicly_accessible=env.rds_publicly_accessible,
    ),
    cluster_services=create_ecs_cluster_services()
)
