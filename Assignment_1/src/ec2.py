from typing import Literal
from mypy_boto3_ec2 import EC2Client


def get_vpc_id(ec2: EC2Client) -> str:
    try:
        print("Getting vcp id...")
        response = ec2.describe_vpcs()
    except Exception as e:
        print(e)
    else:
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
        print(f"vcp id obtained successfully.\n {vpc_id}")
        return vpc_id


def create_security_group(ec2: EC2Client, vpc_id: str, group_name: str) -> str:
    try:
        print("Creating security group...")
        response = ec2.create_security_group(
            GroupName=group_name,
            Description='Allow SSH & HTTP access to the server.',
            VpcId=vpc_id
        )
    except Exception as e:
        print(e)
    else:
        security_group_id = response['GroupId']
        print(f'Security group {security_group_id} created successfully.')
        return security_group_id


def set_security_group_inbound_rules(ec2: EC2Client, security_group_id: str) -> None:
    try:
        print("Setting inbound rules...")
        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',  # Type: SSH
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                 },
                {'IpProtocol': 'tcp',  # Type: HTTP
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                 },
            ]
        )
    except Exception as e:
        print(e)
    else:
        print(f'Inbound rules successfully set for {security_group_id}')


def create_key_pair(ec2: EC2Client, key_name: str) -> None:
    try:
        print("Creating key pair...")
        with open('ec2_keypair.pem', 'w') as file:
            key_pair = ec2.create_key_pair(KeyName=key_name, KeyType='rsa', KeyFormat='pem')
            file.write(key_pair.get('KeyMaterial'))
    except Exception as e:
        print(e)
    else:
        print(f'Key pair {key_pair.get("KeyPairId")} created successfully.')


def launch_ec2_instances(
        ec2: EC2Client,
        image_id: str,
        nbr_instances: int,
        instance_type: Literal["m4.large", "t2.large"],
        key_name: str,
        security_groups: list[str]
) -> list[str]:
    try:
        print("Creating EC2 instances...")
        response = ec2.run_instances(
            ImageId=image_id,
            MinCount=nbr_instances,
            MaxCount=nbr_instances,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroups=security_groups
        )
    except Exception as e:
        print(e)
    else:
        ec2_instances_ids = []
        for instance in response["Instances"]:
            ec2_instances_ids.append(instance["InstanceId"])
        print(f"EC2 instances created successfully.\n {ec2_instances_ids}")
        return ec2_instances_ids


def wait_until_all_running(ec2: EC2Client, instance_ids: list[str]) -> None:
    try:
        print("Waiting until all ec2 instances are running...")
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(
            InstanceIds=instance_ids,
            WaiterConfig={'Delay': 10}  # wait 10s between each attempt.
        )
    except Exception as e:
        print(e)
    else:
        print("All EC2 instances are now running.")
