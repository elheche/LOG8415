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
