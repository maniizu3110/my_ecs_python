from typing import Any, Dict, List, Optional
from services.config.ecs_service import ECSService

from services.config.rds import RDSConfig


class Config:
    def __init__(
        self,
        env: str,
        default_service_name: str,
        pascal_service_name: str,
        vpc_cidr: str,
        rds_config: RDSConfig,
        cdk_env: Optional[Dict[str, Any]] = None,
        domain: Optional[str] = None,
        cluster_services: Optional[List[ECSService]] = None,
        ecr_repository_names: Optional[List[str]] = None,
        secret_manager_names: Optional[List[str]] = None,
        s3_bucket_names: Optional[List[str]] = None,
        waf_config: Optional[Dict[str, Any]] = None
    ) -> None:
        self.env: str = env
        self.cdk_env: Optional[Dict[str, Any]] = cdk_env
        self.domain: Optional[str] = domain
        self.default_service_name: str = default_service_name
        self.pascal_service_name: str = pascal_service_name
        self.cluster_services: Optional[List[ECSService]] = cluster_services
        self.ecr_repository_names: Optional[List[str]] = ecr_repository_names
        self.secret_manager_names: Optional[List[str]] = secret_manager_names
        self.s3_bucket_names: Optional[List[str]] = s3_bucket_names
        self.vpc_cidr: str = vpc_cidr
        self.rds_config: RDSConfig = rds_config
        self.waf_config: Optional[Dict[str, Any]] = waf_config
