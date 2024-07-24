from aws_cdk import (
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    Stack,
    Duration,
    Environment
)
from constructs import Construct

class AlbStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, alb_sg: ec2.SecurityGroup, env: Environment, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)

        self.alb = elbv2.ApplicationLoadBalancer(
            self, "ALB",
            vpc=vpc,
            internet_facing=True,
            security_group=alb_sg,
            load_balancer_name="example-alb"
        )

        self.alb_tg = elbv2.ApplicationTargetGroup(
            self, "TargetGroup",
            vpc=vpc,
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            target_group_name="example-tg",
            health_check=elbv2.HealthCheck(
                path="/",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                healthy_threshold_count=2,
                unhealthy_threshold_count=2
            )
        )

        listener = self.alb.add_listener(
            "Listener",
            port=80,
            open=True,
            default_action=elbv2.ListenerAction.forward([self.alb_tg])
        )
