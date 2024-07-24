from aws_cdk import (
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    Stack,
    Environment
)
from constructs import Construct

class AutoScalingStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, ec2_sg: ec2.SecurityGroup, alb_tg: elbv2.ApplicationTargetGroup, env: Environment, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)

        self.asg = autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            vpc=vpc,
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            security_group=ec2_sg,
            user_data=ec2.UserData.custom(
                """#!/bin/bash
                yum update -y
                amazon-linux-extras install docker -y
                service docker start
                usermod -a -G docker ec2-user
                docker run -d -p 80:80 nginx
                """
            ),
            desired_capacity=1,
            min_capacity=1,
            max_capacity=3
        )

        self.asg.attach_to_application_target_group(alb_tg)
