from typing import List, Dict


class ECSService:
    def __init__(
        self,
        name: str,
        domain_prefix: str,
        image_url: str,
        container_port: int,
        desired_count: int,
        cpu: int,
        memory_limit_mib: int,
        health_check_path: str,
        healthy_http_codes: str
    ) -> None:
        self.name: str = name
        self.domain_prefix: str = domain_prefix
        self.image_url: str = image_url
        self.container_port: int = container_port
        self.desired_count: int = desired_count
        self.cpu: int = cpu
        self.memory_limit_mib: int = memory_limit_mib
        self.health_check_path: str = health_check_path
        self.healthy_http_codes: str = healthy_http_codes
