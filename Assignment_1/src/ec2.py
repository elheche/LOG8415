from typing import Literal

import boto3
from mypy_boto3_ec2 import EC2Client


def create_aws_service(
        aws_service_name: Literal["ec2"],
        aws_region_name: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None
):
    try:
        print(f"Creating {aws_service_name} service...")
        aws_service = boto3.client(
            service_name=aws_service_name,
            region_name=aws_region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )
    except Exception as e:
        print(e)
    else:
        print(f"{aws_service_name} service created successfully.")
        return aws_service


def launch_ec2_instances(ec2: EC2Client, nbr_instances: int, instance_type: Literal["m4.large", "t2.large"]) -> None:
    try:
        print("Creating EC2 instances...")
        ec2.run_instances(
            ImageId="ami-08c40ec9ead489470",  # Ubuntu, 22.04 LTS, 64-bit (x86)
            MinCount=nbr_instances,
            MaxCount=nbr_instances,
            InstanceType=instance_type,
            KeyName="vockey"
        )
    except Exception as e:
        print(e)
    else:
        print("EC2 instances created successfully.")
