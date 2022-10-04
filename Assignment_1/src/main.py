import argparse
from pathlib import Path
from ec2 import create_aws_service, launch_ec2_instances


def main() -> None:
    credentials_exists = Path(f"{Path.home()}/.aws/credentials").is_file()
    config_exists = Path(f"{Path.home()}/.aws/config").is_file()

    if credentials_exists and config_exists:
        ec2 = create_aws_service("ec2")
        launch_ec2_instances(ec2, 4, "m4.large")
        launch_ec2_instances(ec2, 5, "t2.large")
    else:
        parser = argparse.ArgumentParser(
            description=("Program that creates two clusters of virtual machines. "
                         "It first looks for credentials and configuration files provided by your AWS CLI "
                         "(You can configure your AWS CLI using this command: <aws configure>). "
                         "If not found, it offers you the option to manually enter their values using the arguments below:"
                         )
        )
        parser.add_argument("-r", help="The region name for your AWS account.", dest="AWS_REGION_NAME", required=True, nargs=1)
        parser.add_argument("-i", help="The access key for your AWS account.", dest="AWS_ACCESS_KEY_ID", required=True, nargs=1)
        parser.add_argument("-s", help="The secret key for your AWS account.", dest="AWS_SECRET_ACCESS_KEY", required=True, nargs=1)
        parser.add_argument("-t", help="The session key for your AWS account.", dest="AWS_SESSION_TOKEN", required=True, nargs=1)

        args = parser.parse_args()

        ec2 = create_aws_service(
            "ec2",
            args.AWS_REGION_NAME[0],
            args.AWS_ACCESS_KEY_ID[0],
            args.AWS_SECRET_ACCESS_KEY[0],
            args.AWS_SESSION_TOKEN[0]
        )
        launch_ec2_instances(ec2, 4, "m4.large")
        launch_ec2_instances(ec2, 5, "t2.large")


if __name__ == "__main__":
    main()
