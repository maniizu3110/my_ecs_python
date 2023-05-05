from ast import Dict
from typing import Any, Dict, List
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_certificatemanager as acm,
    Stack,
    aws_wafv2 as waf,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
)

from services.config.ecs_service import ECSService


class EcsFargate:
    def __init__(self, stack: Stack, service_name: str, domain: str, vpc: ec2.Vpc, cluster_services: List[ECSService]):
        self.stack = stack
        self.service_name = service_name
        self.domain = domain
        self.vpc = vpc
        self.service_names = service_name
        self.cluster_services: List[ECSService] = cluster_services
        self.fargate_services = []

        # Create ECS cluster
        self.cluster = ecs.Cluster(
            self.stack,
            self.service_name+"Cluster",
            cluster_name=self.service_name,
            vpc=self.vpc
        )

        self.execution_role = iam.Role(
            self.stack,
            "TaskExecutionRoleFor"+self.service_name,
            role_name="TaskExecutionRoleFor"+self.service_name,
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonECSTaskExecutionRolePolicy"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonEC2ContainerRegistryReadOnly")
            ]
        )

        self.lb = elbv2.ApplicationLoadBalancer(
            self.stack,
            self.service_name+"Alb",
            load_balancer_name=self.service_name+"Alb",
            vpc=self.vpc,
            internet_facing=True
        )
        # TODO:ドメインが入力された時、コメントアウト部分が実装されるようにする
        # certificate = acm.Certificate(
        #     self.stack,
        #     self.service_name+"Certificate",
        #     domain_name="*."+self.domain,
        #     validation=acm.CertificateValidation.from_dns(),
        # )

        # listener = self.lb.add_listener(
        #     self.service_name+"Listener",
        #     port=443,
        #     certificates=[elbv2.ListenerCertificate.from_certificate_manager(
        #         acm_certificate=certificate,
        #     )],
        #     protocol=elbv2.ApplicationProtocol.HTTPS,
        #     open=True
        # )
        # listener for port 80
        listener = self.lb.add_listener(
            self.service_name+"Listener",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            open=True
        )

        # # Route 53 A record
        # zone = route53.HostedZone.from_lookup(
        #     self.stack,
        #     self.service_name+"HostedZone",
        #     domain_name=self.domain
        # )

        # Create Fargate Services
        for i, cluster_service in enumerate(self.cluster_services):
            fargate_task_definition = ecs.FargateTaskDefinition(
                self.stack,
                self.service_name + cluster_service.name + "TD",
                execution_role=self.execution_role,
                task_role=self.execution_role,
                cpu=cluster_service.cpu,
                memory_limit_mib=cluster_service.memory_limit_mib,
            )

            fargate_task_definition.add_container(
                self.service_name+cluster_service.name+"Container",
                container_name=cluster_service.name,
                port_mappings=[ecs.PortMapping(
                    container_port=80,
                    host_port=80,
                    protocol=ecs.Protocol.TCP
                )],
                image=ecs.ContainerImage.from_registry(
                    cluster_service.image_url
                ),
                logging=ecs.LogDrivers.aws_logs(
                    stream_prefix=self.service_name+cluster_service.name,
                ),
            )

            fargate_service = ecs.FargateService(
                self.stack,
                self.service_name+cluster_service.name,
                service_name=self.service_name+cluster_service.name,
                cluster=self.cluster,
                desired_count=cluster_service.desired_count,
                task_definition=fargate_task_definition,
            )

            target_group = elbv2.ApplicationTargetGroup(
                self.stack,
                self.service_name+cluster_service.name+"TG",
                target_group_name=self.service_name+cluster_service.name+"TG",
                vpc=self.vpc,
                port=80,
                health_check=elbv2.HealthCheck(
                    path=cluster_service.health_check_path,
                    healthy_http_codes=cluster_service.healthy_http_codes,
                ),
                targets=[fargate_service.load_balancer_target(
                    container_name=cluster_service.name,
                    container_port=80
                )],
            )



            # elbv2.ApplicationListenerRule(
            #     self.stack,
            #     self.service_name+cluster_service.name+"Rule",
            #     priority=1,
            #     listener=listener,
            #     target_groups=[target_group],
            #     conditions=[
            #         elbv2.ListenerCondition.host_headers(
            #             [cluster_service.domain_prefix+"."+self.domain]),
            #     ],
            # )

            # route53.ARecord(
            #     self.stack,
            #     self.service_name+cluster_service.name+"ARecord",
            #     zone=zone,
            #     target=route53.RecordTarget.from_alias(
            #         alias_target=route53_targets.LoadBalancerTarget(self.lb)
            #     ),
            #     record_name=cluster_service.domain_prefix+"."+self.domain,
            # )

            if i == 0:
                listener.add_target_groups(
                    self.service_name+cluster_service.name+"TargetGroup",
                    target_groups=[target_group]
                )

        self.fargate_services.append(fargate_service)

    def create_waf(self, config: Dict[str, Any]):
        # Create WAF web ACL
        self.web_acl = waf.CfnWebACL(
            self.stack,
            config["name"] + "WebACL",
            default_action=waf.CfnWebACL.DefaultActionProperty(
                block={}
            ),
            visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name=self.service_name + "WebACL",
                sampled_requests_enabled=True
            ),
            scope=config["scope"],
            name=self.service_name + "WebACL",
            rules=config["rules"]
        )
        for i, cluster_service in enumerate(self.cluster_services):
            waf.CfnWebACLAssociation(
                self.stack,
                self.service_name +
                cluster_service["name"] + "WAFWebACLAssociation",
                web_acl_arn=self.web_acl.attr_arn,
                resource_arn=self.lb.load_balancer_arn
            )
