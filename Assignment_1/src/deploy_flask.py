import boto3
import jmespath
import paramiko


def get_all_instance() -> list:
    client = boto3.client('ec2')
    response = client.describe_instances()
    public_dns_ip = jmespath.search("Reservations[].Instances[].PublicIpAddress", response)
    print(public_dns_ip)
    return public_dns_ip


if __name__ == "__main__":
    get_all_instance()
