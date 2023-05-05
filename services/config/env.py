from dotenv import load_dotenv
import os
from services.utils.get_repository_name import get_repository_name, change_to_pascal_case, change_to_camel_case


load_dotenv()


class Env:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_region: str,
        env: str,
        github_repository_url: str,
        port: int,
        build_path: str,
        dockerfile_name: str,
        vpc_cidr: str,
        rds_allocated_storage: int,
        rds_instance_type: str,
        rds_deletion_protection: bool,
        rds_publicly_accessible: bool,
        rds_parameters: dict,

    ) -> None:
        self.aws_access_key_id: str = aws_access_key_id
        self.aws_secret_access_key: str = aws_secret_access_key
        self.aws_region: str = aws_region
        self.env: str = env
        self.github_repository_url: str = github_repository_url
        self.port: int = port
        self.build_path: str = build_path
        self.dockerfile_name: str = dockerfile_name
        self.pascal_service_name: str = get_repository_name(
            change_to_pascal_case(github_repository_url))+change_to_camel_case(env)
        self.default_service_name: str = get_repository_name(
            github_repository_url)+"-"+env
        self.vpc_cidr: str = vpc_cidr
        self.rds_allocated_storage: int = rds_allocated_storage
        self.rds_instance_type: str = rds_instance_type
        self.rds_deletion_protection: bool = rds_deletion_protection
        self.rds_publicly_accessible: bool = rds_publicly_accessible
        self.rds_parameters: dict = rds_parameters
