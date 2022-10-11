import boto3
import os
from datetime import date, timedelta, datetime
import json


def save_data(json_file_name, data):
    with open(json_file_name, 'w') as fp:
        json.dumps(data, indent=4, sort_keys=True, default=str)


###################################################################################################################
#                                             Load Balancer CloudWatch metric
###################################################################################################################

def ActiveConnectionCount_metric(cloudwatch_client, lbstring2, yesterday, tomorrow):
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
                                'Value': lbstring2
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
    )

    return response


def ConsumedLCUs_metric(cloudwatch_client, lbstring2, yesterday, tomorrow):
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
                                'Value': lbstring2
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
    )

    return response


def HTTP_Redirect_Count_metric(cloudwatch_client, lbstring2, yesterday, tomorrow):
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
                                'Value': lbstring2
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
    )

    return response


def LB_RequestCount_metric(cloudwatch_client, lbstring2, yesterday, tomorrow):
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
                                'Value': lbstring2
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
    )

    return response


def RuleEvaluations_metric(cloudwatch_client, lbstring2, yesterday, tomorrow):
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
                                'Value': lbstring2
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
    )

    return response


###################################################################################################################
#                                             Targets CloudWatch metric
###################################################################################################################

def HealthyHostCount_metric(cloudwatch_client, tgstring, lbstring2, yesterday, tomorrow):
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
                                'Value': lbstring2
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Average',
                    'Unit': 'Count'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
    )

    return response


def RequestCountPerTarget_metric(cloudwatch_client, tgstring, lbstring2, yesterday, tomorrow):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_RequestCountPerTarget',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'RequestCountPerTarget',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring2
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Average',
                    'Unit': 'Count'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
    )

    return response


def TargetConnectionErrorCount_metric(cloudwatch_client, tgstring, lbstring2, yesterday, tomorrow):
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
                                'Value': lbstring2
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Average',
                    'Unit': 'Count'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
    )

    return response


def TargetResponseTime_metric(cloudwatch_client, tgstring, lbstring2, yesterday, tomorrow):
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
                                'Value': lbstring2
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Average',
                    'Unit': 'Count'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
    )

    return response


def UnHealthyHostCount_metric(cloudwatch_client, tgstring, lbstring2, yesterday, tomorrow):
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
                                'Value': lbstring2
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Average',
                    'Unit': 'Count'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
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

    yesterday = date.today() - timedelta(days=2)
    tomorrow = date.today() + timedelta(days=2)

    data = ActiveConnectionCount_metric(cloudwatch, lbstring2=lbstring2, yesterday=yesterday, tomorrow=tomorrow)
    save_data("Cloudwatch/Load_balancer/ActiveConnectionCount_metric.json", data)

    data = HTTP_Redirect_Count_metric(cloudwatch, lbstring2=lbstring2, yesterday=yesterday, tomorrow=tomorrow)
    save_data("Cloudwatch/Load_balancer/HTTP_Redirect_Count_metric.json", data)

    data = LB_RequestCount_metric(cloudwatch, lbstring2=lbstring2, yesterday=yesterday, tomorrow=tomorrow)
    save_data("Cloudwatch/Load_balancer/RequestCount_metric.json", data)

    data = RuleEvaluations_metric(cloudwatch, lbstring2=lbstring2, yesterday=yesterday, tomorrow=tomorrow)
    save_data("Cloudwatch/Load_balancer/RuleEvaluations_metric.json", data)

    print("Saving Load balancer CloudWatch metrics is done ....")


def targets_metrics(cloudwatch, mytargetgrouparn, loadBalancerARN, target_grp_number):
    print("Start saving targets CloudWatch metrics ....")

    tgarray = mytargetgrouparn.split(':')
    tgstring = tgarray[-1]

    lbarray = loadBalancerARN.split(':')
    lbstring = lbarray[-1]
    lbarray2 = lbstring.split('/')
    lbstring2 = lbarray2[1] + '/' + lbarray2[2] + '/' + lbarray2[3]

    yesterday = date.today() - timedelta(days=2)
    tomorrow = date.today() + timedelta(days=2)

    data = HealthyHostCount_metric(cloudwatch, tgstring=tgstring, lbstring2=lbstring2, yesterday=yesterday,
                                   tomorrow=tomorrow)
    save_data("Cloudwatch/targets/target_grp_" + str(target_grp_number) + "/HealthyHostCount_metric.json", data)

    data = RequestCountPerTarget_metric(cloudwatch, tgstring=tgstring, lbstring2=lbstring2, yesterday=yesterday,
                                        tomorrow=tomorrow)
    save_data("Cloudwatch/targets/target_grp_" + str(target_grp_number) + "/RequestCountPerTarget_metric.json", data)

    data = TargetConnectionErrorCount_metric(cloudwatch, tgstring=tgstring, lbstring2=lbstring2, yesterday=yesterday,
                                             tomorrow=tomorrow)
    save_data("Cloudwatch/targets/target_grp_" + str(target_grp_number) + "/TargetConnectionErrorCount_metric.json",
              data)

    data = TargetResponseTime_metric(cloudwatch, tgstring=tgstring, lbstring2=lbstring2, yesterday=yesterday,
                                     tomorrow=tomorrow)
    save_data("Cloudwatch/targets/target_grp_" + str(target_grp_number) + "/TargetResponseTime_metric.json", data)

    data = UnHealthyHostCount_metric(cloudwatch, tgstring=tgstring, lbstring2=lbstring2, yesterday=yesterday,
                                     tomorrow=tomorrow)
    save_data("Cloudwatch/targets/target_grp_" + str(target_grp_number) + "/UnHealthyHostCount_metric.json", data)

    print("Saving targets CloudWatch metrics is done ....")
