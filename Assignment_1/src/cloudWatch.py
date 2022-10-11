import boto3
import os
from datetime import date, timedelta, datetime
import json


def RequestCount_metric(cloudwatch_client, tgstring, lbstring2, yesterday, tomorrow):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest',
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

def ActiveConnectionCount_metric(cloudwatch_client, tgstring, lbstring2, yesterday, tomorrow):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest',
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


def TargetResponseTime_metric(cloudwatch_client, tgstring, lbstring2, yesterday, tomorrow):

    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest',
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


def save_data(json_file_name, data):
    with open(json_file_name, 'w') as fp:
        json.dumps(data, indent=4, sort_keys=True, default=str)


def save_metrics(cloudwatch, mytargetgrouparn=None, loadBalancerARN=None):
    if mytargetgrouparn is not None:
        tgarray = mytargetgrouparn.split(':')
        tgstring = tgarray[-1]

    if loadBalancerARN is not None:
        lbarray = loadBalancerARN.split(':')
        lbstring = lbarray[-1]
        lbarray2 = lbstring.split('/')
        lbstring2 = lbarray2[1] + '/' + lbarray2[2] + '/' + lbarray2[3]

    yesterday = date.today() - timedelta(days=2)
    tomorrow = date.today() + timedelta(days=2)

    data = RequestCount_metric(cloudwatch, tgstring=tgstring, lbstring2=lbstring2, yesterday=yesterday, tomorrow=tomorrow)
    save_data("RequestCount_metric.json", data)

    data = ActiveConnectionCount_metric(cloudwatch, tgstring=tgstring, lbstring2=lbstring2, yesterday=yesterday, tomorrow=tomorrow)
    save_data("ActiveConnectionCount.json", data)

    data = TargetResponseTime_metric(cloudwatch, tgstring=tgstring, lbstring2=lbstring2, yesterday=yesterday, tomorrow=tomorrow)
    save_data("TargetResponseTime_metric.json", data)

    print("done")