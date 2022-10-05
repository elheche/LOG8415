from mypy_boto3_elbv2 import ElasticLoadBalancingv2Client


def create_target_group(elbv2: ElasticLoadBalancingv2Client, target_group_name: str, vpc_id: str) -> str:
    try:
        print("Creating target group...")
        response = elbv2.create_target_group(
            Name=target_group_name,
            Protocol="HTTP",
            ProtocolVersion="HTTP1",
            Port=80,
            VpcId=vpc_id,
            HealthCheckProtocol="HTTP",
            TargetType='instance',
            IpAddressType='ipv4'
        )
    except Exception as e:
        print(e)
    else:
        target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
        print(f'Target group {target_group_arn} created successfully.')
        return target_group_arn


def register_targets(elbv2: ElasticLoadBalancingv2Client, target_group_arn: str, targets: list[dict]) -> None:
    try:
        print("Registering targets...")
        elbv2.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=targets
        )
    except Exception as e:
        print(e)
    else:
        print(f'Targets {targets} registered successfully to group target {target_group_arn}.')


def create_application_load_balancer(elbv2: ElasticLoadBalancingv2Client, subnets: list[str], security_groups: list[str]):
    try:
        print("Creating application load_balancer...")
        response = elbv2.create_load_balancer(
            Name='log8415-lab1-elb',
            Subnets=subnets,
            SecurityGroups=security_groups,
            Scheme="internet-facing",
            Type="application",
            IpAddressType="ipv4"
        )
    except Exception as e:
        print(e)
    else:
        alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
        print(f'Application load balancer {alb_arn} created successfully.')
        return alb_arn
