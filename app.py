#!/usr/bin/env python3
from aws_cdk import App, Stack
from services.ecr import ECRRepositories
from services.ecs import EcsFargate
from services.network import Network
from services.rds import RDS
from services.s3 import S3Buckets
from services.config.config import Config
from services._lambda import BasicAuth
from setup import config
import boto3


def get_latest_ecr_image_url(repository_name: str) -> str:
    ecr_client = boto3.client('ecr')
    try:
        response = ecr_client.describe_images(repositoryName=repository_name)
        if len(response['imageDetails']) > 0:
            latest_image = sorted(
                response['imageDetails'], key=lambda x: x['imagePushedAt'], reverse=True)[0]
            registry_id = latest_image['registryId']
            region = config.cdk_env['region']
            return f"{registry_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{latest_image['imageTags'][0]}"
        else:
            return ""
    except ecr_client.exceptions.RepositoryNotFoundException:
        return ""


class MyServiceStack:
    def __init__(self, app: App, config: Config):
        self.stack = Stack(
            app,
            config.default_service_name,
            env=config.cdk_env
        )

        S3Buckets(self.stack, config)
        ECRRepositories(self.stack, config.ecr_repository_names, config.env)

        self.vpc = Network(
            self.stack, config).get_vpc()

        RDS(self.stack, config.pascal_service_name, self.vpc,
            config.rds_config).create_rds()

        # if config.waf_config:
        #     self.ecs.create_waf(config.waf_config)
        # BasicAuth(self.stack, config.default_service_name, self.vpc)
        latest_image_url = get_latest_ecr_image_url(
            config.default_service_name)
        if latest_image_url:
            config.cluster_services[0].image_url = latest_image_url
            self.ecs = EcsFargate(
                self.stack,
                config.default_service_name,
                config.domain,
                self.vpc,
                config.cluster_services
            )


app = App()
MyServiceStack(app, config)
app.synth()
