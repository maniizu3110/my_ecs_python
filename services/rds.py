from typing import Dict
from aws_cdk import (
    aws_rds as rds,
    aws_ec2 as ec2,
    Stack
)

from services.config.rds import RDSConfig


class RDS:
    def __init__(self, stack: Stack, service_name: str, vpc: ec2.Vpc, rds_config: RDSConfig):
        self.stack = stack
        self.service_name = service_name
        self.vpc = vpc
        self.database_name = rds_config.database_name
        self.engine = rds_config.engine
        self.instance_type = rds_config.instance_type
        self.allocated_storage = rds_config.allocated_storage
        self.deletion_protection = rds_config.deletion_protection
        self.publicly_accessible = rds_config.publicly_accessible
        self.parameters = rds_config.parameters

    def create_rds(self):
        sg = ec2.SecurityGroup(self.stack, "SecurityGroupRDS", vpc=self.vpc)
        # Allow inbound traffic from the app subnets
        sg.add_ingress_rule(
            ec2.Peer.ipv4(self.vpc.vpc_cidr_block),
            ec2.Port.tcp(3306),
            "Allow app instances to connect to RDS instances"
        )

        parameter_groups = rds.ParameterGroup(
            self.stack, self.service_name+"ParameterGroup",
            engine=self.engine,
            parameters=self.parameters
        )
        rds.DatabaseInstance(
            self.stack,
            self.service_name+"RDS",
            instance_identifier=self.service_name,
            engine=self.engine,
            security_groups=[sg],
            publicly_accessible=self.publicly_accessible,
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnets=self.vpc.public_subnets if self.publicly_accessible else self.vpc.private_subnets),
            allocated_storage=self.allocated_storage,
            database_name=self.service_name,
            instance_type=self.instance_type,
            deletion_protection=self.deletion_protection,
            parameter_group=parameter_groups
        )
