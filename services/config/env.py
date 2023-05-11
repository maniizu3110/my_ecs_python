from dotenv import load_dotenv
import os
from services.utils.get_repository_name import change_to_pascal_case, change_to_camel_case


load_dotenv()


class Env:
    def __init__(
        self,
        service_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_region: str,
        env: str,
        github_repository_url: str,
        port: int,
        build_path: str,
        domain: str,
        dockerfile_name: str,
        vpc_cidr: str,
        pre_build_script: str,
        database_kind: str,
        health_check_path: str,
        health_check_codes: str,
        rds_allocated_storage: int,
        rds_instance_type: str,
        rds_deletion_protection: bool,
        rds_publicly_accessible: bool,
    ) -> None:
        self.aws_access_key_id: str = aws_access_key_id
        self.aws_secret_access_key: str = aws_secret_access_key
        self.aws_region: str = aws_region
        self.env: str = env
        self.github_repository_url: str = github_repository_url
        self.port: int = port
        self.build_path: str = build_path
        self.domain: str = domain
        self.dockerfile_name: str = dockerfile_name
        self.database_kind: str = database_kind
        self.health_check_path: str = health_check_path
        self.health_check_codes: str = health_check_codes
        self.pascal_service_name: str = change_to_pascal_case(
            service_name)+change_to_camel_case(env)
        self.default_service_name: str = service_name+"-"+env
        self.vpc_cidr: str = vpc_cidr
        self.pre_build_script: str = pre_build_script
        self.rds_allocated_storage: int = rds_allocated_storage
        self.rds_instance_type: str = rds_instance_type
        self.rds_deletion_protection: bool = rds_deletion_protection
        self.rds_publicly_accessible: bool = rds_publicly_accessible
