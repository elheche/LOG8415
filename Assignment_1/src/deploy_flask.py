from datetime import time

import boto3
import jmespath
import paramiko
from constants import *


# KEY_PAIR = "/Assignment_1/src/ec2_keypair.pem"


def get_all_instance_ip() -> list:
    client = boto3.client('ec2')
    response = client.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        },
    ], )

    public_dns_ip = jmespath.search("Reservations[].Instances[].PublicIpAddress", response)
    print(public_dns_ip)
    return public_dns_ip


def ssh_connexion(ssh, instance_ip, retries) -> None:
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
        './ec2_keypair.pem')
    interval = 5
    try:
        retries += 1
        print('SSH into the instance: {}'.format(instance_ip))
        ssh.connect(hostname=instance_ip,
                    username='ubuntu', pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(instance_ip))
        ssh_connexion(ssh, instance_ip, retries)


def main() -> None:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    public_ip = get_all_instance_ip()
    for ip in public_ip:
        ssh_connexion(ssh, ip, 0)
        stdin, stdout, stderr = ssh.exec_command("echo 'Hello World!'")
        print('stdout:', stdout.read())
        print('stderr:', stderr.read())


if __name__ == "__main__":
    main()
