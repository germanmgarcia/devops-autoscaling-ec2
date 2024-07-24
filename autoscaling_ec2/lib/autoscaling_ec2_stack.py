from aws_cdk import (
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as autoscaling,
    aws_rds as rds,
    Stack,
    CfnOutput,
    Environment
)
from constructs import Construct

from vpc_stack import VpcStack
from security_groups_stack import SecurityGroupsStack
from alb_stack import AlbStack
from autoscaling_stack import AutoScalingStack
from rds_stack import RdsStack

class AutoScalingEc2Stack(Stack):

    def __init__(self, scope: Construct, id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)

        vpc_stack = VpcStack(self, "VpcStack", env=env)
        security_groups_stack = SecurityGroupsStack(self, "SecurityGroupsStack", vpc=vpc_stack.vpc, env=env)
        alb_stack = AlbStack(self, "AlbStack", vpc=vpc_stack.vpc, alb_sg=security_groups_stack.alb_sg, env=env)
        autoscaling_stack = AutoScalingStack(self, "AutoScalingStack", vpc=vpc_stack.vpc, ec2_sg=security_groups_stack.ec2_sg, alb_tg=alb_stack.alb_tg, env=env)
        rds_stack = RdsStack(self, "RdsStack", vpc=vpc_stack.vpc, rds_sg=security_groups_stack.rds_sg, env=env)

        CfnOutput(self, "VPCID", value=vpc_stack.vpc.vpc_id)
        CfnOutput(self, "PublicSubnetIDs", value=",".join([subnet.subnet_id for subnet in vpc_stack.vpc.public_subnets]))
        CfnOutput(self, "PrivateSubnetIDs", value=",".join([subnet.subnet_id for subnet in vpc_stack.vpc.private_subnets]))
        CfnOutput(self, "ALBDnsName", value=alb_stack.alb.load_balancer_dns_name)
        CfnOutput(self, "RdsEndpoint", value=rds_stack.db_instance.db_instance_endpoint_address)
