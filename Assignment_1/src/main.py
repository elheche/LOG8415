import argparse
from pathlib import Path

from cloudWatch import *
from code_deploy import *
from constants import *
from ec2 import *
from elb import *
from iam import *
from s3 import *
from sts import *
from init_aws_service import *


def main() -> None:
    ###################################################################################################################
    #                                    Initializing AWS services
    ###################################################################################################################
    credentials_exists = Path(f'{Path.home()}/.aws/credentials').is_file()
    config_exists = Path(f'{Path.home()}/.aws/config').is_file()

    if credentials_exists and config_exists:
        # Initialize ec2, elbv2, CodeDeploy, iam, s3, sts services with default credentials and configuration
        ec2 = create_aws_service(EC2_CONFIG['Common']['ServiceName'])
        elbv2 = create_aws_service(ELB_V2_CONFIG['Common']['ServiceName'])
        code_deploy = create_aws_service(CODE_DEPLOY_CONFIG['Common']['ServiceName'])
        cloud_watch = create_aws_service(CLOUD_WATCH_CONFIG['Common']['ServiceName'])
        iam = create_aws_service(IAM_CONFIG['Common']['ServiceName'])
        s3 = create_aws_service('s3')
        sts = create_aws_service('sts')
    else:
        parser = argparse.ArgumentParser(
            description=('Program that creates two clusters of virtual machines. '
                         'It first looks for credentials and configuration files provided by your AWS CLI '
                         '(You can configure your AWS CLI using this command: <aws configure>). '
                         'If not found, it offers you the option to manually enter their values using '
                         'the arguments below:'
                         )
        )
        parser.add_argument('-r', help='The region name for your AWS account.', dest='AWS_REGION_NAME', required=True, nargs=1)
        parser.add_argument('-i', help='The access key for your AWS account.', dest='AWS_ACCESS_KEY_ID', required=True, nargs=1)
        parser.add_argument('-s', help='The secret key for your AWS account.', dest='AWS_SECRET_ACCESS_KEY', required=True, nargs=1)
        parser.add_argument('-t', help='The session key for your AWS account.', dest='AWS_SESSION_TOKEN', required=True, nargs=1)

        args = parser.parse_args()

        user_credentials_config = [
            args.AWS_REGION_NAME[0],
            args.AWS_ACCESS_KEY_ID[0],
            args.AWS_SECRET_ACCESS_KEY[0],
            args.AWS_SESSION_TOKEN[0]
        ]

        # Initialize ec2, elbv2, CodeDeploy, iam, s3, sts services with user credentials and configuration
        ec2 = create_aws_service(EC2_CONFIG['Common']['ServiceName'], *user_credentials_config)
        elbv2 = create_aws_service(ELB_V2_CONFIG['Common']['ServiceName'], *user_credentials_config)
        code_deploy = create_aws_service(CODE_DEPLOY_CONFIG['Common']['ServiceName'], *user_credentials_config)
        cloud_watch = create_aws_service(CLOUD_WATCH_CONFIG['Common']['ServiceName'], *user_credentials_config)
        iam = create_aws_service(IAM_CONFIG['Common']['ServiceName'], *user_credentials_config)
        s3 = create_aws_service(S3_CONFIG['Common']['ServiceName'], *user_credentials_config)
        sts = create_aws_service(STS_CONFIG['Common']['ServiceName'], *user_credentials_config)

    ###################################################################################################################
    #                                    Creating and Configuring Clusters & Load Balancer
    ###################################################################################################################

    # TODO: Do we need to create a VPC specific to this assignment or using the default one ?
    vpc_id = get_vpc_id(ec2)

    # We'll use LabRole (a default role) since we can't create a new one (needed to give permissions to CodeDeploy).
    role_arn = get_role(iam, IAM_CONFIG['Common']['RoleName'])

    # Create a security group and set its inbound rules to accept HTTP and SSH connections
    security_group_id = create_security_group(ec2, vpc_id, EC2_CONFIG['Common']['SecurityGroups'][0])
    set_security_group_inbound_rules(ec2, security_group_id)

    # Create a key pair
    key_pair_id = create_key_pair(ec2, EC2_CONFIG['Common']['KeyPairName'])

    # Create 4 instances of m4.large for Cluster 1
    ec2_instance_ids_1 = []
    for instance_tag_id in range(1, 5):
        ec2_instance_ids_1.append(
            launch_ec2_instance(ec2, EC2_CONFIG['Common'] | EC2_CONFIG['Cluster1'], str(instance_tag_id))
        )

    # Create 5 instances of t2.large for Cluster 2
    ec2_instance_ids_2 = []
    for instance_tag_id in range(5, 10):
        ec2_instance_ids_2.append(
            launch_ec2_instance(ec2, EC2_CONFIG['Common'] | EC2_CONFIG['Cluster2'], str(instance_tag_id))
        )

    # Wait until all ec2 instance states pass to 'running'
    wait_until_all_running(ec2, ec2_instance_ids_1 + ec2_instance_ids_2)

    # Create two target groups: Cluster1 and Cluster2
    target_group_arn_1 = create_target_group(elbv2, ELB_V2_CONFIG['Cluster1']['TargetGroupName'], vpc_id)
    target_group_arn_2 = create_target_group(elbv2, ELB_V2_CONFIG['Cluster2']['TargetGroupName'], vpc_id)

    # Register m4.large instances to Cluster1
    register_targets(elbv2, target_group_arn_1, ec2_instance_ids_1)
    # Register 't2.large' instances to Cluster2
    register_targets(elbv2, target_group_arn_2, ec2_instance_ids_2)

    # Create an application load balancer
    subnet_ids = get_subnet_ids(ec2, vpc_id, [EC2_CONFIG['Cluster1']['AvailabilityZone'], EC2_CONFIG['Cluster2']['AvailabilityZone']])
    alb_arn = create_application_load_balancer(elbv2, subnet_ids, [security_group_id])

    # Create an ALB listener
    alb_listener_arn = create_alb_listener(elbv2, alb_arn, [target_group_arn_1, target_group_arn_2])

    # Create rule 1 in the last listener to forward requests to cluster 1
    alb_listener_rule_1_arn = create_alb_listener_rule(
        elbv2,
        alb_listener_arn,
        target_group_arn_1,
        ELB_V2_CONFIG['Cluster1']['PathPattern'],
        ELB_V2_CONFIG['Cluster1']['RulePriority']
    )

    # Create rule 2 in the last listener to forward requests to cluster 2
    alb_listener_rule_2_arn = create_alb_listener_rule(
        elbv2,
        alb_listener_arn,
        target_group_arn_2,
        ELB_V2_CONFIG['Cluster2']['PathPattern'],
        ELB_V2_CONFIG['Cluster2']['RulePriority']
    )

    ###################################################################################################################
    #                                             Deploying Flask Application
    ###################################################################################################################

    # Get aws user account
    aws_user_account = get_aws_user_account(sts)

    # Create an S3 bucket
    create_bucket(s3, S3_CONFIG['Common']['Bucket'])

    # Set bucket policies (give user and CodeDeploy access to bucket)
    put_bucket_policy(s3, S3_CONFIG['Common'], aws_user_account, role_arn)

    # Upload the server app to the created bucket
    upload_server_app_to_s3_bucket(s3, S3_CONFIG['Common']['Bucket'])

    # Create an application to deploy to Cluster1 and Cluster2
    application_id = create_application(code_deploy, CODE_DEPLOY_CONFIG['Common']['ApplicationName'])

    # Create two deployment groups Cluster1 and Cluster 2 to target ec2 instances that belong to these clusters
    deployment_group_id_1 = create_deployment_group(
        code_deploy,
        CODE_DEPLOY_CONFIG['Common'] | CODE_DEPLOY_CONFIG['Cluster1'],
        role_arn
    )

    deployment_group_id_2 = create_deployment_group(
        code_deploy,
        CODE_DEPLOY_CONFIG['Common'] | CODE_DEPLOY_CONFIG['Cluster2'],
        role_arn
    )

    # Launch two app deployments, the first deploys to Cluster1, the second deploys to Cluster2
    deployment_id_1 = create_deployment(
        code_deploy,
        CODE_DEPLOY_CONFIG['Common'] | CODE_DEPLOY_CONFIG['Cluster1']
    )

    deployment_id_2 = create_deployment(
        code_deploy,
        CODE_DEPLOY_CONFIG['Common'] | CODE_DEPLOY_CONFIG['Cluster2']
    )

    ###################################################################################################################
    #                                             Code to Run Docker Image to Request Clusters
    ###################################################################################################################

    # Put code here

    ###################################################################################################################
    #                                             Getting CloudWatch Metrics
    ###################################################################################################################
    # save metrics for load balancer
    load_balancer_metrics(cloud_watch, alb_arn)

    # save metrics for target group 1
    targets_metrics(cloud_watch, target_group_arn_1, alb_arn, 1)

    # save metrics for target group 2
    targets_metrics(cloud_watch, target_group_arn_2, alb_arn, 2)

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
