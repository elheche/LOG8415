from mypy_boto3_codedeploy import CodeDeployClient


def create_application(code_deploy: CodeDeployClient, application_name: str) -> str:
    try:
        print('Creating application...')
        response = code_deploy.create_application(
            applicationName=application_name,
            computePlatform='Server'
        )
    except Exception as e:
        print(e)
    else:
        application_id = response['applicationId']
        print(f'Application {application_id} created successfully.')
        return application_id


def create_deployment_group(code_deploy: CodeDeployClient, code_deploy_config: dict, service_role_arn: str) -> str:
    try:
        print('Creating deployment group...')
        response = code_deploy.create_deployment_group(
            applicationName=code_deploy_config['ApplicationName'],
            deploymentGroupName=code_deploy_config['DeploymentGroupName'],
            deploymentConfigName=code_deploy_config['DeploymentConfigName'],
            ec2TagFilters=code_deploy_config['EC2TagFilters'],
            serviceRoleArn=service_role_arn,
            autoRollbackConfiguration=code_deploy_config['AutoRollbackConfiguration'],
            deploymentStyle=code_deploy_config['DeploymentStyle']
        )
    except Exception as e:
        print(e)
    else:
        deployment_group_id = response['deploymentGroupId']
        print(f'Deployment group {deployment_group_id} created successfully.')
        return deployment_group_id
