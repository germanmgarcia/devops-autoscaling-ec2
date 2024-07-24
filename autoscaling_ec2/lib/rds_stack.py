from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    Stack,
    Environment,
    SecretValue,
    RemovalPolicy
)
from constructs import Construct

class RdsStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, rds_sg: ec2.SecurityGroup, env: Environment, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)

        subnet_group = rds.SubnetGroup(
            self, "RdsSubnetGroup",
            vpc=vpc,
            description="Subnet group for RDS",
            subnet_group_name="main",
            vpc_subnets=ec2.SubnetSelection(subnets=vpc.private_subnets)
        )

        self.db_instance = rds.DatabaseInstance(
            self, "RdsInstance",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_13_11
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=vpc.private_subnets),
            security_groups=[rds_sg],
            allocated_storage=20,
            storage_type=rds.StorageType.GP2,
            database_name="exampledb",
            credentials=rds.Credentials.from_password(
                username="adminexample", password=SecretValue.unsafe_plain_text("password")
            ),
            parameter_group=rds.ParameterGroup.from_parameter_group_name(
                self, "ParameterGroup", "default.postgres13"
            ),
            publicly_accessible=False,
            delete_automated_backups=True,
            removal_policy=RemovalPolicy.DESTROY
        )
