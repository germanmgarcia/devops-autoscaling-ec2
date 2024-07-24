from aws_cdk import (
    aws_ec2 as ec2,
    Stack,
    Environment
)
from constructs import Construct

class SecurityGroupsStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, env: Environment, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)

        self.alb_sg = ec2.SecurityGroup(
            self, "ALBSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="ALBSecurityGroup"
        )

        self.alb_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP traffic from anywhere"
        )

        self.ec2_sg = ec2.SecurityGroup(
            self, "EC2SecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="EC2SecurityGroup"
        )

        self.ec2_sg.add_ingress_rule(
            peer=self.alb_sg,
            connection=ec2.Port.tcp(80),
            description="Allow HTTP traffic from ALB"
        )

        self.rds_sg = ec2.SecurityGroup(
            self, "RDSSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="RDSSecurityGroup"
        )

        self.rds_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4("10.0.0.0/16"),
            connection=ec2.Port.tcp(5432),
            description="Allow PostgreSQL traffic from VPC"
        )
