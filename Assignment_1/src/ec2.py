import boto3


def create_ec2_instances(
        aws_region_name: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None
) -> None:
    try:
        print("Creating EC2 instances...")
        resource_ec2 = boto3.client(
            service_name="ec2",
            region_name=aws_region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )
        resource_ec2.run_instances(
            ImageId="ami-08c40ec9ead489470",  # Ubuntu, 22.04 LTS, 64-bit (x86)
            MinCount=4,
            MaxCount=4,
            InstanceType="t2.large",
            KeyName="vockey"
        )
    except Exception as e:
        print(e)
    else:
        print("EC2 instances created successfully.")
