import argparse
from pathlib import Path

from cloudWatch import *
from constants import *
from ec2 import *
from elb import *
from init_aws_service import *


def main() -> None:
    # credentials_exists = Path(f'{Path.home()}/.aws/credentials').is_file()
    # config_exists = Path(f'{Path.home()}/.aws/config').is_file()
    #
    # if credentials_exists and config_exists:
    #     # Initialize ec2, elbv2 services with default credentials and configuration
    #     ec2 = create_aws_service(EC2_CONFIG['Common']['ServiceName'])
    #     elbv2 = create_aws_service(ELB_V2_CONFIG['Common']['ServiceName'])
    # else:
    #     parser = argparse.ArgumentParser(
    #         description=('Program that creates two clusters of virtual machines. '
    #                      'It first looks for credentials and configuration files provided by your AWS CLI '
    #                      '(You can configure your AWS CLI using this command: <aws configure>). '
    #                      'If not found, it offers you the option to manually enter their values using '
    #                      'the arguments below:'
    #                      )
    #     )
    #     parser.add_argument('-r', help='The region name for your AWS account.', dest='AWS_REGION_NAME', required=True, nargs=1)
    #     parser.add_argument('-i', help='The access key for your AWS account.', dest='AWS_ACCESS_KEY_ID', required=True, nargs=1)
    #     parser.add_argument('-s', help='The secret key for your AWS account.', dest='AWS_SECRET_ACCESS_KEY', required=True, nargs=1)
    #     parser.add_argument('-t', help='The session key for your AWS account.', dest='AWS_SESSION_TOKEN', required=True, nargs=1)
    #
    #     args = parser.parse_args()
    #
    #     # Initialize ec2, elbv2 services with user credentials and configuration
    #     ec2 = create_aws_service(
    #         EC2_CONFIG['Common']['ServiceName'],
    #         args.AWS_REGION_NAME[0],
    #         args.AWS_ACCESS_KEY_ID[0],
    #         args.AWS_SECRET_ACCESS_KEY[0],
    #         args.AWS_SESSION_TOKEN[0]
    #     )
    #
    #     elbv2 = create_aws_service(
    #         ELB_V2_CONFIG['Common']['ServiceName'],
    #         args.AWS_REGION_NAME[0],
    #         args.AWS_ACCESS_KEY_ID[0],
    #         args.AWS_SECRET_ACCESS_KEY[0],
    #         args.AWS_SESSION_TOKEN[0]
    #     )
    #
    # ###################################################################################################################
    # #                                             Creating and Configuring Clusters & Load Balancer
    # ###################################################################################################################
    #
    # # TODO: Do we need to create a VPC specific to this assignment or using the default one ?
    # vpc_id = get_vpc_id(ec2)
    #
    # # Create a security group and set its inbound rules to accept HTTP and SSH connections
    # security_group_id = create_security_group(ec2, vpc_id, EC2_CONFIG['Common']['SecurityGroups'][0])
    # set_security_group_inbound_rules(ec2, security_group_id)
    #
    # # Create a key pair
    # key_pair_id = create_key_pair(ec2, EC2_CONFIG['Common']['KeyPairName'])
    #
    # # Create 4 instances of m4.large for Cluster 1
    # ec2_instance_ids_1 = launch_ec2_instances(ec2, EC2_CONFIG['Common'] | EC2_CONFIG['Cluster1'])
    #
    # # Create 5 instances of t2.large for Cluster 2
    # ec2_instance_ids_2 = launch_ec2_instances(ec2, EC2_CONFIG['Common'] | EC2_CONFIG['Cluster2'])
    #
    # # Wait until all ec2 instance states pass to 'running'
    # wait_until_all_running(ec2, ec2_instance_ids_1 + ec2_instance_ids_2)
    #
    # # Create two target groups: Cluster1 and Cluster2
    # target_group_arn_1 = create_target_group(elbv2, ELB_V2_CONFIG['Cluster1']['TargetGroupName'], vpc_id)
    # target_group_arn_2 = create_target_group(elbv2, ELB_V2_CONFIG['Cluster2']['TargetGroupName'], vpc_id)
    #
    # # Register m4.large instances to Cluster1
    # register_targets(elbv2, target_group_arn_1, ec2_instance_ids_1)
    # # Register 't2.large' instances to Cluster2
    # register_targets(elbv2, target_group_arn_2, ec2_instance_ids_2)
    #
    # # Create an application load balancer
    # subnet_ids = get_subnet_ids(ec2, vpc_id, [EC2_CONFIG['Cluster1']['AvailabilityZone'], EC2_CONFIG['Cluster2']['AvailabilityZone']])
    # alb_arn = create_application_load_balancer(elbv2, subnet_ids, [security_group_id])
    #
    # # Create an ALB listener
    # alb_listener_arn = create_alb_listener(elbv2, alb_arn, [target_group_arn_1, target_group_arn_2])
    #
    # # Create rule 1 in the last listener to forward requests to cluster 1
    # alb_listener_rule_1_arn = create_alb_listener_rule(
    #     elbv2,
    #     alb_listener_arn,
    #     target_group_arn_1,
    #     ELB_V2_CONFIG['Cluster1']['PathPattern'],
    #     ELB_V2_CONFIG['Cluster1']['RulePriority']
    # )
    #
    # # Create rule 2 in the last listener to forward requests to cluster 2
    # alb_listener_rule_2_arn = create_alb_listener_rule(
    #     elbv2,
    #     alb_listener_arn,
    #     target_group_arn_2,
    #     ELB_V2_CONFIG['Cluster2']['PathPattern'],
    #     ELB_V2_CONFIG['Cluster2']['RulePriority']
    # )

    ###################################################################################################################
    #                                             Deploying Flask Applications
    ###################################################################################################################

    # Put code here

    ###################################################################################################################
    #                                             Getting CloudWatch Metrics
    ###################################################################################################################
    # cloudwatch = boto3.client('cloudwatch', region_name= args.AWS_REGION_NAME[0],
    #                           aws_access_key_id= args.AWS_ACCESS_KEY_ID[0],
    #                           aws_secret_access_key = args.AWS_SECRET_ACCESS_KEY[0],
    #                           aws_session_token= args.AWS_SESSION_TOKEN[0]
    #                           )

    cloudwatch = boto3.client('cloudwatch', region_name= "us-east-1",
                              aws_access_key_id= "ASIAVQW6TG7UDPS4JTTG",
                              aws_secret_access_key ="aXIOjGhj5v6sPAsxulloN5gR1BTNUf2z3lveDrD0",
                              aws_session_token= "FwoGZXIvYXdzEK3//////////wEaDL/Y9uyvaLZdXHl1jyLCAYiOK9nhJ9OlCw/aBGiXQnud3Ahx9lzt9Lv32toPCyhb7vPEB/no3acnMIicuQqvWnZq7+DPCU10f3K/aJFKCg/s4HdADcxqAwM20Vk2HUFPpOvra+hkSqLhayDLbplM8n7E7SdcZEmN6XCOzbaFWC8To18pzrfqAMFITJNk09SSZOVGXjyEC38JKtUFa+YRdIowdSjRiByNUde1a8EoySLWfTet+/T0GTaeHyVLLc5yKxJBaA9eC9jUozvfol1QrPzrKIfykZoGMi3ZHxatQJVPkvQnBsfwcY0B+2RYcSyVd3bpcSIJ+2NXGu/yBNAnsF5ULBRmWKk="
                              )
    save_metrics(cloudwatch,"arn:aws:elasticloadbalancing:us-east-1:379497691112:targetgroup/Cluster1/b0114e56715a0cbb")

    save_metrics(cloudwatch,target_group_arn_1)
    save_metrics(cloudwatch, target_group_arn_1)

    ###################################################################################################################
    #                                             Code to Run Docker Image to Request Clusters
    ###################################################################################################################

    # Put code here

    ###################################################################################################################
    #                                             Deleting Everything
    ###################################################################################################################

    # Delete rule 1
    delete_alb_listener_rule(elbv2, rule_arn=alb_listener_rule_1_arn)

    # Delete rule 2
    delete_alb_listener_rule(elbv2, rule_arn=alb_listener_rule_2_arn)

    # Delete the application load balancer (this will delete the ALB listener
    delete_application_load_balancer(elbv2, load_balancer_arn=alb_arn)

    # Delete Target Group 1
    delete_target_group(elbv2, target_group_arn=target_group_arn_1)

    # Delete Target Group 2
    delete_target_group(elbv2, target_group_arn=target_group_arn_2)

    # Terminate all instances of t2.large and m4.large
    terminate_ec2_instances(ec2, ec2_instances_ids=ec2_instance_ids_1 + ec2_instance_ids_2)

    # Delete Key Pair
    delete_key_pair(ec2, key_pair_id=key_pair_id)

    # Delete Security Group
    delete_security_group(ec2, security_group_id=security_group_id)


if __name__ == '__main__':
    main()
