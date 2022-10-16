import boto3
import os
from datetime import date, timedelta, datetime, timezone
import json
import os


def save_data(json_file_name, data):
    dir = json_file_name[:json_file_name.rfind('/')]
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(json_file_name, 'w') as fp:
        json.dump(data, fp, indent=4, sort_keys=True, default=str)


###################################################################################################################
#                                             Load Balancer CloudWatch metric
###################################################################################################################
def RequestCount_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_RequestCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'RequestCount',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def ActiveConnectionCount_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_ActiveConnectionCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'ActiveConnectionCount',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def ConsumedLCUs_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_ConsumedLCUs',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'ConsumedLCUs',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def HTTP_Redirect_Count_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_HTTP_Redirect_Count',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'HTTP_Redirect_Count',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def LB_RequestCount_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_RequestCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'RequestCount',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def RuleEvaluations_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_RuleEvaluations',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'RuleEvaluations',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


###################################################################################################################
#                                             Targets CloudWatch metric
###################################################################################################################

def HealthyHostCount_metric(cloudwatch_client, tgstring, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_HealthyHostCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'HealthyHostCount',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Average',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def RequestCountPerTarget_metric(cloudwatch_client, tgstring, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_RequestCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'RequestCount',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def TargetConnectionErrorCount_metric(cloudwatch_client, tgstring, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_TargetConnectionErrorCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'TargetConnectionErrorCount',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def TargetResponseTime_metric(cloudwatch_client, tgstring, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_TargetResponseTime',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'TargetResponseTime',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Average',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def UnHealthyHostCount_metric(cloudwatch_client, tgstring, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_UnHealthyHostCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'UnHealthyHostCount',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Average',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


###################################################################################################################
#                                             Run metrics loaders
###################################################################################################################
def load_balancer_metrics(cloudwatch, loadBalancerARN):
    print("Start saving Load balancer CloudWatch metrics ....")

    lbarray = loadBalancerARN.split(':')
    lbstring = lbarray[-1]
    lbarray2 = lbstring.split('/')
    lbstring2 = lbarray2[1] + '/' + lbarray2[2] + '/' + lbarray2[3]

    now = datetime.now(timezone.utc)
    StartTime = datetime(now.year, now.month, now.day, now.hour - 1)
    EndTime = datetime(now.year, now.month, now.day + 1, now.hour + 1)

    data = RequestCount_metric(cloudwatch, lbstring=lbstring2, StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/load_balancer/request_count_metric.json", data)

    data = ActiveConnectionCount_metric(cloudwatch, lbstring=lbstring2,  StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/load_balancer/active_connection_count_metric.json", data)

    data = ConsumedLCUs_metric(cloudwatch, lbstring=lbstring2,  StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/load_balancer/consumed_lcus_metric.json", data)

    data = HTTP_Redirect_Count_metric(cloudwatch, lbstring=lbstring2, StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/load_balancer/http_redirect_count_metric.json", data)

    data = LB_RequestCount_metric(cloudwatch, lbstring=lbstring2,  StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/load_balancer/request_count_metric.json", data)

    data = RuleEvaluations_metric(cloudwatch, lbstring=lbstring2,  StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/load_balancer/rule_evaluations_metric.json", data)

    print("Saving Load balancer CloudWatch metrics is done ....")


def targets_metrics(cloudwatch, mytargetgrouparn, loadBalancerARN, target_grp_number):
    print("Start saving targets CloudWatch metrics ....")

    tgarray = mytargetgrouparn.split(':')
    tgstring = tgarray[-1]

    lbarray = loadBalancerARN.split(':')
    lbstring = lbarray[-1]
    lbarray2 = lbstring.split('/')
    lbstring2 = lbarray2[1] + '/' + lbarray2[2] + '/' + lbarray2[3]

    now = datetime.now(timezone.utc)
    StartTime = datetime(now.year, now.month, now.day, now.hour - 1)
    EndTime = datetime(now.year, now.month, now.day, now.hour + 1)

    data = HealthyHostCount_metric(cloudwatch, tgstring=tgstring, lbstring=lbstring2,  StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/targets/target_grp_" + str(target_grp_number) + "/healthy_host_count_metric.json", data)

    data = RequestCountPerTarget_metric(cloudwatch, tgstring=tgstring, lbstring=lbstring2,  StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/targets/target_grp_" + str(target_grp_number) + "/request_count_per_target_metric.json", data)

    data = TargetConnectionErrorCount_metric(cloudwatch, tgstring=tgstring, lbstring=lbstring2,  StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/targets/target_grp_" + str(target_grp_number) + "/target_connection_error_count_metric.json",
              data)

    data = TargetResponseTime_metric(cloudwatch, tgstring=tgstring, lbstring=lbstring2, StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/targets/target_grp_" + str(target_grp_number) + "/target_response_time_metric.json", data)

    data = UnHealthyHostCount_metric(cloudwatch, tgstring=tgstring, lbstring=lbstring2,  StartTime=StartTime, EndTime= EndTime)
    save_data("cloudwatch/targets/target_grp_" + str(target_grp_number) + "/unhealthy_host_count_metric.json", data)

    print("Saving targets CloudWatch metrics is done ....")
