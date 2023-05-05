from aws_cdk import (
    aws_lambda as _lambda,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elb,
    Stack
)

# ALBとの紐付けは手動で行う必要がある
# labmda内に記述するコードはbasic_authディレクトリに配置されている
# 参考：https://qiita.com/shonansurvivors/items/422924e720eb3465b865


class BasicAuth:
    def __init__(self, stack: Stack, service_name: str, vpc: ec2.Vpc) -> None:
        self.function = _lambda.Function(
            stack, f"{service_name}BasicAuth",
            function_name=f"{service_name}BasicAuth",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("basic_auth"),
            vpc=vpc
        )
