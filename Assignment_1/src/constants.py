EC2_CONFIG = {
    'Common': {
        'ServiceName': 'ec2',
        'ImageId': 'ami-08c40ec9ead489470',  # Ubuntu, 22.04 LTS, 64-bit (x86)
        'KeyPairName': 'log8415_lab1_kp',
        'SecurityGroups': ['log8415_lab1_sg'],
    },
    'Cluster1': {
        'InstanceCount': 4,
        'InstanceType': 'm4.large',
        'AvailabilityZone': 'us-east-1a',
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Cluster', 'Value': '1', }]
            }
        ]
    },
    'Cluster2': {
        'InstanceCount': 5,
        'InstanceType': 't2.large',
        'AvailabilityZone': 'us-east-1b',
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Cluster', 'Value': '2', }]
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
        'PathPattern': '/cluster1/*',
        'RulePriority': 1
    },
    'Cluster2': {
        'TargetGroupName': 'Cluster2',
        'PathPattern': '/cluster2/*',
        'RulePriority': 2
    }
}
