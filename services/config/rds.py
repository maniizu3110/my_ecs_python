from typing import Dict
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds


class RDSConfig:
    def __init__(
        self,
        database_name: str,
        engine: rds.DatabaseInstanceEngine,
        instance_type: ec2.InstanceType,
        allocated_storage: int,
        parameters: Dict[str, str] = {},
        deletion_protection: bool = True,
        publicly_accessible: bool = True
    ) -> None:
        self.database_name: str = database_name
        self.parameters: Dict[str, str] = parameters
        self.engine: rds.DatabaseInstanceEngine = engine
        self.instance_type: ec2.InstanceType = instance_type
        self.allocated_storage: int = allocated_storage
        self.deletion_protection: bool = deletion_protection
        self.publicly_accessible: bool = publicly_accessible
