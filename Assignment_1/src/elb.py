from mypy_boto3_elbv2 import ElasticLoadBalancingv2Client


def create_target_group(
        elbv2: ElasticLoadBalancingv2Client,
        target_group_name: str,
        vpc_id: str
) -> str:
    try:
        print('Creating target group...')
        response = elbv2.create_target_group(
            Name=target_group_name,
            Protocol='HTTP',
            ProtocolVersion='HTTP1',
            Port=80,
            VpcId=vpc_id,
            HealthCheckProtocol='HTTP',
            TargetType='instance',
            IpAddressType='ipv4'
        )
    except Exception as e:
        print(e)
    else:
        target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
        print(f'Target group {target_group_arn} created successfully.')
        return target_group_arn


def register_targets(
        elbv2: ElasticLoadBalancingv2Client,
        target_group_arn: str,
        ec2_instance_ids: list[str]
) -> None:
    try:
        print('Registering targets...')
        elbv2.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[{'Id': ec2_instance_id, 'Port': 80} for ec2_instance_id in ec2_instance_ids]
        )
    except Exception as e:
        print(e)
    else:
        print(f'Targets {ec2_instance_ids} registered successfully to group target {target_group_arn}.')


def create_application_load_balancer(
        elbv2: ElasticLoadBalancingv2Client,
        subnets: list[str],
        security_group_ids: list[str]
) -> str:
    try:
        print('Creating application load_balancer...')
        response = elbv2.create_load_balancer(
            Name='log8415-lab1-elb',
            Subnets=subnets,
            SecurityGroups=security_group_ids,
            Scheme='internet-facing',
            Type='application',
            IpAddressType='ipv4'
        )
    except Exception as e:
        print(e)
    else:
        alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
        print(f'Application load balancer {alb_arn} created successfully.')
        return alb_arn


def create_alb_listener(
        elbv2: ElasticLoadBalancingv2Client,
        alb_arn: str,
        target_group_arns: list[str]
) -> str:
    try:
        print('Creating alb listener...')
        response = elbv2.create_listener(
            LoadBalancerArn=alb_arn,
            Protocol='HTTP',
            Port=80,
            DefaultActions=[
                {
                    'Type': 'forward',
                    'ForwardConfig': {
                        'TargetGroups': [
                            {
                                'TargetGroupArn': target_group_arns[0],
                                'Weight': 50
                            },
                            {
                                'TargetGroupArn': target_group_arns[1],
                                'Weight': 50
                            }
                        ]
                    }
                }
            ]
        )
    except Exception as e:
        print(e)
    else:
        alb_listener_arn = response['Listeners'][0]['ListenerArn']
        print(f'ALB listener {alb_listener_arn} created successfully.')
        return alb_listener_arn


def create_alb_listener_rule(
        elbv2: ElasticLoadBalancingv2Client,
        alb_listener_arn: str,
        target_group_arn: str,
        path_pattern: str,
        priority: int
) -> str:
    try:
        print('Creating alb listener rule...')
        response = elbv2.create_rule(
            ListenerArn=alb_listener_arn,
            Conditions=[
                {
                    'Field': 'path-pattern',
                    'Values': [
                        path_pattern
                    ]
                }
            ],
            Priority=priority,
            Actions=[
                {
                    'Type': 'forward',
                    'TargetGroupArn': target_group_arn
                }
            ]
        )
    except Exception as e:
        print(e)
    else:
        alb_listener_rule_arn = response['Rules'][0]['RuleArn']
        print(f'ALB listener rule {alb_listener_rule_arn} created successfully.')
        return alb_listener_rule_arn


def delete_alb_listener_rule(
        elbv2: ElasticLoadBalancingv2Client,
        rule_arn: str,
) -> None:
    try:
        print('Deleting ALB listener rule...')
        response = elbv2.delete_rule(
            RuleArn=rule_arn
        )
    except Exception as e:
        print(e)
    else:
        print(response)
        print(f'ALB listener rule deleted successfully.')


def delete_application_load_balancer(
        elbv2: ElasticLoadBalancingv2Client,
        load_balancer_arn: str,
) -> None:
    try:
        print('Deleting application load_balancer...')
        response = elbv2.delete_load_balancer(
            LoadBalancerArn=load_balancer_arn
        )
    except Exception as e:
        print(e)
    else:
        print(response)
        print(f'Application load balancer deleted successfully.')


def delete_target_group(
        elbv2: ElasticLoadBalancingv2Client,
        target_group_arn: str,
) -> None:
    try:
        print('Deleting target group...')
        response = elbv2.delete_target_group(
            TargetGroupArn=target_group_arn
        )
    except Exception as e:
        print(e)
    else:
        print(response)
        print(f'Target Group deleted successfully.')
