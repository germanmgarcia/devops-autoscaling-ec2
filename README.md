# AWS Infrastructure Deployment with Terraform

## Overview
This Terraform configuration deploys the following AWS infrastructure:
- A VPC with a public and a private subnet.
- An Internet Gateway attached to the VPC.
- An Application Load Balancer (ALB) with a security group.
- An Auto Scaling Group (ASG) with EC2 instances running an application.
- An RDS instance for database storage, located in a private subnet.



## Deployment Instructions
1. **Configure AWS Credentials:**
   Ensure you have your AWS credentials configured either by using AWS CLI (`aws configure`) or by setting environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID="your_access_key_id"
   export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
   export AWS_DEFAULT_REGION="your_aws_region"
