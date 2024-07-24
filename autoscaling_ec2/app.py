#!/usr/bin/env python3
import sys
from os import path

sys.path.append(path.join(path.dirname(path.abspath(__file__)), 'lib'))

from aws_cdk import App, Environment
from autoscaling_ec2_stack import AutoScalingEc2Stack

app = App()

account = app.node.try_get_context("account")
region = app.node.try_get_context("region")

env = Environment(account=account, region=region)

AutoScalingEc2Stack(app, "AutoScalingEc2Stack", env=env)
app.synth()
