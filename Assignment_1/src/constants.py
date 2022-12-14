EC2_CONFIG = {
    'Common': {
        'ServiceName': 'ec2',
        'ImageId': 'ami-0ee23bfc74a881de5',  # Ubuntu, 18.04 LTS, 64-bit (x86) (CodeDeploy Agent preinstalled)
        'KeyPairName': 'log8415_lab1_kp',
        'SecurityGroups': ['log8415_lab1_sg'],
        'InstanceCount': 1,
        'InstanceProfileName': 'LabInstanceProfile',  # We'll use this default role since we can't create a new one.
        'MetadataOptions': {
            'InstanceMetadataTags': 'enabled'
        }
    },
    'Cluster1': {
        'InstanceType': 'm4.large',
        'AvailabilityZone': 'us-east-1a',
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Cluster', 'Value': '1', },
                    {'Key': 'Instance', 'Value': '', }  # Instance tag value is given when creating the instance
                ]
            }
        ]
    },
    'Cluster2': {
        'InstanceType': 't2.large',
        'AvailabilityZone': 'us-east-1b',
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Cluster', 'Value': '2', },
                    {'Key': 'Instance', 'Value': '', }  # Instance tag value is given when creating the instance
                ]
            }
        ]
    }
}

ELB_V2_CONFIG = {
    'Common': {
        'ServiceName': 'elbv2',
        'SecurityGroups': ['log8415_lab1_sg']
    },
    'Cluster1': {
        'TargetGroupName': 'Cluster1',
        'PathPattern': '/cluster1*',
        'RulePriority': 1
    },
    'Cluster2': {
        'TargetGroupName': 'Cluster2',
        'PathPattern': '/cluster2*',
        'RulePriority': 2
    }
}

CODE_DEPLOY_CONFIG = {
    'Common': {
        'ServiceName': 'codedeploy',
        'ApplicationName': 'log8415_lab1_app',
        'DeploymentConfigName': 'CodeDeployDefault.OneAtATime',
        'AutoRollbackConfiguration': {
            'enabled': True,
            'events': ['DEPLOYMENT_FAILURE']
        },
        'DeploymentStyle': {
            'deploymentType': 'IN_PLACE',
            'deploymentOption': 'WITHOUT_TRAFFIC_CONTROL'
        },
        'Revision': {
            'revisionType': 'S3',
            's3Location': {
                'key': 'server.zip',
                'bundleType': 'zip',
            }
        }
    },
    'Cluster1': {
        'DeploymentGroupName': 'Cluster1',
        'EC2TagFilters': [
            {
                'Key': 'Cluster',
                'Value': '1',
                'Type': 'KEY_AND_VALUE'
            },
        ]
    },
    'Cluster2': {
        'DeploymentGroupName': 'Cluster2',
        'EC2TagFilters': [
            {
                'Key': 'Cluster',
                'Value': '2',
                'Type': 'KEY_AND_VALUE'
            },
        ]
    }
}

IAM_CONFIG = {
    'Common': {
        'ServiceName': 'iam',
        'RoleName': 'LabRole'  # We'll use this default role since we can't create a new one.
    }
}

S3_CONFIG = {
    'Common': {
        'ServiceName': 's3',
        'Bucket': 'log8415-lab1-bucket-',
        'BucketPolicy': {
            "Statement": [
                {
                    "Action": ["s3:PutObject"],
                    "Effect": "Allow",
                },
                {
                    "Action": [
                        "s3:Get*",
                        "s3:List*"
                    ],
                    "Effect": "Allow",
                }
            ]
        }
    }
}

STS_CONFIG = {
    'Common': {
        'ServiceName': 'sts'
    }
}

CLOUD_WATCH_CONFIG = {
    'Common': {
        'ServiceName': 'cloudwatch'
    }
}
