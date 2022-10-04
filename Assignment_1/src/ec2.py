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


def get_vpc_id(ec2: EC2Client):
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs')[0].get('VpcId')
    return vpc_id


def create_security_group(ec2: EC2Client, vpc_id: str) -> str:
    try:
        response = ec2.create_security_group(
            GroupName='log8415_lab1',
            Description='Allow SSH access to the server.',
            VpcId=vpc_id
        )
    except Exception as e:
        print(e)
    else:
        security_group_id = response['GroupId']
        print(f'Security group {security_group_id} created successfully.')
        return security_group_id


def set_security_group_inbound_rules(ec2: EC2Client, security_group_id: str):
    try:
        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',  # Type: SSH
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                 }
            ]
        )
    except Exception as e:
        print(e)
    else:
        print(f'Inbound rules successfully set for {security_group_id}')
