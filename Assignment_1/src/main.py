import argparse
from pathlib import Path
from botocore.exceptions import WaiterError
from cloudWatch import *
from code_deploy import *
from constants import *
from ec2 import *
from elb import *
from iam import *
from init_aws_service import *
from s3 import *
from sts import *
import sys
from test_scenarios.send_get_requests import run_test_scenario_with_multithreading
import docker


def main() -> None:
    ###################################################################################################################
    #                                    Setting program arguments
    ###################################################################################################################

    parser = argparse.ArgumentParser(
        description=('Program that creates two clusters of virtual machines and deploys a flask app to them.'
                     'It first looks for credentials and configuration files provided by your AWS CLI '
                     '(You can configure your AWS CLI using this command: <aws configure>). '
                     'If not found, it offers you the option to manually enter their values using '
                     'the arguments below:'
                     )
    )

    sub_parser = parser.add_subparsers(title='aws arguments', dest='AWS')
    aws_parser = sub_parser.add_parser('aws')

    parser.add_argument('-r', '--reset', help="reset user's aws account.", dest='RESET', required=False, action='store_true')
    parser.add_argument('-d', '--docker', help="enable test scenarios through docker.", dest='DOCKER', required=False,
                        action='store_true')
    aws_parser.add_argument('-g', '--region', help='region name for your AWS account.', dest='AWS_REGION_NAME', required=True, nargs=1)
    aws_parser.add_argument('-i', '--id', help='access key for your AWS account.', dest='AWS_ACCESS_KEY_ID', required=True, nargs=1)
    aws_parser.add_argument('-s', '--secret', help='secret key for your AWS account.', dest='AWS_SECRET_ACCESS_KEY', required=True, nargs=1)
    aws_parser.add_argument('-t', '--token', help='session key for your AWS account.', dest='AWS_SESSION_TOKEN', required=True, nargs=1)

    args = parser.parse_args()

    ###################################################################################################################
    #                                    Initializing AWS services
    ###################################################################################################################

    if args.AWS:
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

    else:
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
            parser.error('default aws credentials and configuration not found.')
            sys.exit(1)

    ###################################################################################################################
    #                                    Resetting AWS account
    ###################################################################################################################

    if args.RESET:
        reset(ec2, elbv2, s3, code_deploy)
        sys.exit(0)

    ###################################################################################################################
    #                                    Creating and Configuring Clusters & Load Balancer
    ###################################################################################################################

    # Get the default vpc id
    vpc_id = get_vpc_id(ec2)

    # We'll use LabRole (a default role) since we can't create a new one (needed to give permissions to CodeDeploy).
    role_arn = get_role(iam, IAM_CONFIG['Common']['RoleName'])

    # Create a security group and set its inbound rules to accept HTTP and SSH connections
    security_group_id = create_security_group(ec2, vpc_id, EC2_CONFIG['Common']['SecurityGroups'][0])
    set_security_group_inbound_rules(ec2, security_group_id)

    # Save security group id to aws_data (needed to reset aws account)
    aws_data = {'SecurityGroupId': security_group_id}

    # Create a key pair
    key_pair_id = create_key_pair(ec2, EC2_CONFIG['Common']['KeyPairName'])

    # Save key pair id to aws_data (needed to reset aws account)
    aws_data['KeyPairId'] = key_pair_id

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

    # Save ec2 instance ids to aws_data (needed to reset aws account)
    aws_data['EC2InstanceIds'] = ec2_instance_ids_1 + ec2_instance_ids_2

    # Wait until all ec2 instance states pass to 'running'
    wait_until_all_ec2_instance_are_running(ec2, ec2_instance_ids_1 + ec2_instance_ids_2)

    # Create two target groups: Cluster1 and Cluster2
    target_group_arn_1 = create_target_group(elbv2, ELB_V2_CONFIG['Cluster1']['TargetGroupName'], vpc_id)
    target_group_arn_2 = create_target_group(elbv2, ELB_V2_CONFIG['Cluster2']['TargetGroupName'], vpc_id)

    # Save target group arns to aws_data (needed to reset aws account)
    aws_data['TargetGroups'] = [target_group_arn_1, target_group_arn_2]

    # Register m4.large instances to Cluster1
    register_targets(elbv2, target_group_arn_1, ec2_instance_ids_1)
    # Register 't2.large' instances to Cluster2
    register_targets(elbv2, target_group_arn_2, ec2_instance_ids_2)

    # Create an application load balancer
    subnet_ids = get_subnet_ids(ec2, vpc_id, [EC2_CONFIG['Cluster1']['AvailabilityZone'], EC2_CONFIG['Cluster2']['AvailabilityZone']])
    alb_arn, alb_dns_name = create_application_load_balancer(elbv2, subnet_ids, [security_group_id])

    # Save alb arn to aws_data (needed to reset aws account)
    aws_data['AlbArn'] = alb_arn

    # Create an ALB listener
    alb_listener_arn = create_alb_listener(elbv2, alb_arn, [target_group_arn_1, target_group_arn_2])

    # Save alb listener arn to aws_data (needed to reset aws account)
    aws_data['AlbListenerArn'] = alb_listener_arn

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

    # Save rule ARNs to aws_data (needed to reset aws account)
    aws_data['RuleArns'] = [alb_listener_rule_1_arn, alb_listener_rule_2_arn]

    ###################################################################################################################
    #                                             Deploying Flask Application
    ###################################################################################################################

    # Get aws user account
    aws_user_account = get_aws_user_account(sts)

    # Create an S3 bucket
    bucket = create_bucket(s3, S3_CONFIG['Common']['Bucket'])

    # Save bucket name to aws_data (needed to reset aws account)
    aws_data['Bucket'] = bucket

    # Set bucket policies (give user and CodeDeploy access to bucket)
    put_bucket_policy(s3, S3_CONFIG['Common'], bucket, aws_user_account, role_arn)

    # Upload the server app to the created bucket
    upload_server_app_to_s3_bucket(s3, bucket)

    # Create an application to deploy to Cluster1 and Cluster2
    create_application(code_deploy, CODE_DEPLOY_CONFIG['Common']['ApplicationName'])

    # Save application name to aws_data (needed to reset aws account)
    aws_data['ApplicationName'] = CODE_DEPLOY_CONFIG['Common']['ApplicationName']

    # Create two deployment groups Cluster1 and Cluster 2 to target ec2 instances that belong to these clusters
    create_deployment_group(
        code_deploy,
        CODE_DEPLOY_CONFIG['Common'] | CODE_DEPLOY_CONFIG['Cluster1'],
        role_arn
    )

    create_deployment_group(
        code_deploy,
        CODE_DEPLOY_CONFIG['Common'] | CODE_DEPLOY_CONFIG['Cluster2'],
        role_arn
    )

    # Launch two app deployments, the first deploys to Cluster1, the second deploys to Cluster2
    deployment_id_cluster_1 = create_deployment(
        code_deploy,
        bucket,
        CODE_DEPLOY_CONFIG['Common'] | CODE_DEPLOY_CONFIG['Cluster1']
    )

    deployment_id_cluster_2 = create_deployment(
        code_deploy,
        bucket,
        CODE_DEPLOY_CONFIG['Common'] | CODE_DEPLOY_CONFIG['Cluster2']
    )

    # Export aws_data to aws_data.json file (needed to execute -r/--reset command)
    save_aws_data(aws_data, 'aws_data.json')

    ###################################################################################################################
    #                                             Code to Run Docker Image to Request Clusters
    ###################################################################################################################

    code_deploy_waiter = code_deploy.get_waiter('deployment_successful')

    try:
        print("deployment in progress ...")
        code_deploy_waiter.wait(
            deploymentId=deployment_id_cluster_1,
            WaiterConfig={
                'Delay': 15,
                'MaxAttempts': 120
            }
        )
    except WaiterError as e:
        print(e)
    except Exception as e:
        print(e)
    else:
        try:
            code_deploy_waiter.wait(
                deploymentId=deployment_id_cluster_2,
                WaiterConfig={
                    'Delay': 15,
                    'MaxAttempts': 120
                }
            )
        except WaiterError as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            print("deployment done successfully ...")

    if args.DOCKER:
        # Running Test scenario for Cluster 1 and Cluster 2 through Docker

        print("Performing test scenarios ...")
        print("Creating Dockerfile ...")
        f = open("./test_scenarios/Dockerfile", "w")
        f.write("FROM python:3 \n")
        f.write("ADD send_get_requests.py / \n")
        f.write("RUN pip install requests \n")
        f.write(f'CMD [ "python", "./send_get_requests.py", "--dns",  "{alb_dns_name}"] \n')
        f.close()

        docker_client = docker.from_env()
        print("Building docker image ...")
        docker_client.images.build(path="./test_scenarios", tag="log8415-test-scenarios")
        print("Running docker container ...")
        container_output = docker_client.containers.run("log8415-test-scenarios")
        print(container_output)
    else:

        # Running Test scenario for Cluster 1 without Docker

        print("Performing test scenarios ...")
        _, time_cluster_1 = run_test_scenario_with_multithreading(scenarios=[1, 2],
                                                                  url="http://" + alb_dns_name + "/cluster1",
                                                                  headers={"Content-Type": "application/json"})

        # Running Test scenario for Cluster 2 without Docker
        _, time_cluster_2 = run_test_scenario_with_multithreading(scenarios=[1, 2],
                                                                  url="http://" + alb_dns_name + "/cluster2",
                                                                  headers={"Content-Type": "application/json"})

        print("test_scenario for Cluster 1 done in ", time_cluster_1, "seconds")
        print("test_scenario for Cluster 1 done in ", time_cluster_2, "seconds")

    ###################################################################################################################
    #                                             Getting CloudWatch Metrics
    ###################################################################################################################

    # save metrics for load balancer
    load_balancer_metrics(cloud_watch, alb_arn)

    # save metrics for target group 1
    targets_metrics(cloud_watch, target_group_arn_1, alb_arn, 1)

    # save metrics for target group 2
    targets_metrics(cloud_watch, target_group_arn_2, alb_arn, 2)


def save_aws_data(aws_data: dict, path: str) -> None:
    try:
        print('Saving aws data...')
        with open(path, 'w') as file:
            json.dump(aws_data, file)
    except Exception as e:
        print(e)
        sys.exit(1)
    else:
        print(f'AWS data saved successfully to {path}.')


def load_aws_data(path: str) -> dict:
    try:
        print('Loading aws data...')
        with open(path, 'r') as file:
            aws_data = json.load(file)
    except Exception as e:
        print(e)
        sys.exit(1)
    else:
        print(f'AWS data loaded successfully.\n{aws_data}')
        return aws_data


def reset(
        ec2: EC2Client,
        elbv2: ElasticLoadBalancingv2Client,
        s3: S3Client,
        code_deploy: CodeDeployClient
) -> None:
    data_exists = Path('aws_data.json').is_file()

    if data_exists:
        aws_data = load_aws_data('aws_data.json')
        terminate_ec2_instances(ec2, aws_data['EC2InstanceIds'])
        wait_until_all_ec2_instances_are_terminated(ec2, aws_data['EC2InstanceIds'])
        for rule_arn in aws_data['RuleArns']:
            delete_alb_listener_rule(elbv2, rule_arn)
        delete_alb_listener(elbv2, aws_data['AlbListenerArn'])
        delete_application_load_balancer(elbv2, aws_data['AlbArn'])
        wait_until_alb_is_deleted(elbv2, aws_data['AlbArn'])
        for target_group_arn in aws_data['TargetGroups']:
            delete_target_group(elbv2, target_group_arn)
        delete_key_pair(ec2, aws_data['KeyPairId'])
        delete_security_group(ec2, aws_data['SecurityGroupId'])
        delete_server_app_from_s3_bucket(s3, aws_data['Bucket'])
        delete_bucket(s3, aws_data['Bucket'])
        delete_application(code_deploy, aws_data['ApplicationName'])
        print('AWS account successfully reset.')
    else:
        print('aws_data.json file not found.')


if __name__ == '__main__':
    main()
