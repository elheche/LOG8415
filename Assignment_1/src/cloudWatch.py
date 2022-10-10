import boto3
import os
from datetime import date, timedelta, datetime
import json


def access_last_days_data_metric(cloudwatch_client, targetGroupARN, loadBalancerARN, days):
    if targetGroupARN is not None:
        tgarray = targetGroupARN.split(':')
        tgstring = tgarray[-1]

    if loadBalancerARN is not None:
        lbarray = loadBalancerARN.split(':')
        lbstring = lbarray[-1]
        lbarray2 = lbstring.split('/')
        lbstring2 = lbarray2[1] + '/' + lbarray2[2] + '/' + lbarray2[3]
    yesterday = date.today() - timedelta(days=days)
    tomorrow = date.today() + timedelta(days=1)

    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest',
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
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Microseconds'
                }
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
    )

    # return response['MetricDataResults'][0]['Values']
    return response


def save_data(stats):
    with open('data.json', 'w') as fp:
        json.dump(stats, fp)


def save_metrics(cloudwatch, mytargetgrouparn=None, myapplicationlbarn=None):
    stats = access_last_days_data_metric(cloudwatch, mytargetgrouparn, myapplicationlbarn, 2)
    save_data(stats)
