from aws_cdk import aws_ecr as ecr, Stack


class ECRRepositories:
    def __init__(self, stack: Stack, ecr_repository_names: list[str], env: str):
        for name in ecr_repository_names:
            ecr.Repository(
                stack, f"{env}-{name}", repository_name=name, image_scan_on_push=True)
