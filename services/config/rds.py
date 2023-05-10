from typing import Dict
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds

from services.utils.rds_setting import get_rds_engine, get_rds_parameters


class RDSConfig:
    def __init__(
        self,
        database_name: str,
        kind: str,
        instance_type: ec2.InstanceType,
        allocated_storage: int,
        deletion_protection: bool = True,
        publicly_accessible: bool = True
    ) -> None:
        self.database_name: str = database_name
        self.engine: rds.DatabaseInstanceEngine = get_rds_engine(kind)
        self.instance_type: ec2.InstanceType = instance_type
        self.allocated_storage: int = allocated_storage
        self.deletion_protection: bool = deletion_protection
        self.publicly_accessible: bool = publicly_accessible
        self.parameters: Dict[str, str] = get_rds_parameters(kind)
