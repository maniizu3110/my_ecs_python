from aws_cdk import (
    aws_ec2 as ec2,
    Stack,
)
from services.config.config import Config


class Network:
    def __init__(self, stack: Stack, config: Config):
        self.stack = stack
        self.service_name = config.default_service_name
        self.vcp_cidr = config.vpc_cidr
        self.vpc = ec2.Vpc(
            self.stack,
            self.service_name+"Vpc",
            vpc_name=self.service_name+"Vpc",
            cidr=self.vcp_cidr,
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", cidr_mask=24, subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(
                    name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            ],
            nat_gateways=1
        )

        # Create two private subnets
        self.private_subnet_1 = self.vpc.private_subnets[0]
        self.private_subnet_2 = self.vpc.private_subnets[1]

        # Create two public subnets
        self.public_subnet_1 = self.vpc.public_subnets[0]
        self.public_subnet_2 = self.vpc.public_subnets[1]

    def get_vpc(self) -> ec2.Vpc:
        return self.vpc
