from account_configs import account_configs
from sts import get_assumed_role_credentials
from cloudfront import list_deployed_distributions
from cloudwatch import get_metric_statistics
from sns_main import run_sns_operations
from alarm import Alarm
import json

# Get a list of all subaccounts and their associated metrics.

def subaccounts_and_metrics_alarm(account_configs):
    all_metrics = []

    for config in account_configs:
        assume_role_arn = f'arn:aws:iam::{config["account_id"]}:role/{config["role"]}'
        assumed_role_credentials = get_assumed_role_credentials(assume_role_arn)

        print(f"AccountId {config['account_id']} {config['account_name']}")
        # List all CloudFront distributions
        distributions = list_deployed_distributions(assumed_role_credentials)
        threshold = config['threshold']
        for distribution in distributions:
            print(f"DistributionId {distribution['Id']}")
            metric_statistics = get_metric_statistics(assumed_role_credentials, distribution, config['minutes'], config['period'], 'Sum')
            consecutive_high_points = 0
            all_metrics = []
            data_points = metric_statistics['Datapoints']
            for point in data_points:
                # If the values of consecutive_points consecutive data points in the loop are all greater than or equal to threshold,
                # then send a message to SNS

                if point['Sum'] >= threshold:
                    consecutive_high_points += 1
                    # Append metrics to the list
                    all_metrics.append({
                        'StartTime': metric_statistics['StartTime'],
                        'EndTime': metric_statistics['EndTime'],
                        'Datapoint': point
                    })
                    sum_str = ','.join(str(metric['Datapoint']['Sum']) for metric in all_metrics)
                    print(f"{sum_str}")
                else:
                    consecutive_high_points = 0
                    all_metrics = []

                print(f"consecutive_high_points： {consecutive_high_points}, {point['Sum']}")
                if consecutive_high_points >= config['consecutive_points']:
                    print(f"-----prepare send email-------")
                    # Send SNS message here

                    # 在linkedAccount上发送告警
                    # sns = boto3.client('sns',
                    #                     aws_access_key_id=aws_access_key_id,
                    #                     aws_secret_access_key=aws_secret_access_key,
                    #                     aws_session_token=aws_session_token)

                    # 在payer账号发送告警
                    alarm = Alarm()
                    alarm.name = f"High request metrics for account: {config['account_id']}"
                    alarm.description = f"Threshold Crossed: 1 out of the last 1 {point} was greater than the threshold {threshold} (minimum {consecutive_high_points} datapoint for OK -> ALARM transition)."
                    alarm.aws_account = config['account_id']
                    alarm.timestamp = point['Timestamp']
                    alarm.state_change = "OK -> ALARM"
                    alarm.datapoints = all_metrics
                    alarm.threshold = {
                        "metric_name": metric_statistics['MetricName'],
                        "metric_namespace": metric_statistics['Namespace'],
                        "period": metric_statistics['Period'],
                        "extended_statistic": "Sum",
                        "unit": None,
                        "threshold": threshold,
                        "comparison_operator": "GreaterThanThreshold",
                        "evaluation_periods": consecutive_high_points

                    }
                    alarm.state_change_actions={
                        "Action1": "ALARM",
                        "Action2": "executor-default" # optional 如禁用资源，可以使用executor-default
                    }
                    run_sns_operations(config['payer_topic_name'], json.dumps(alarm.__dict__, indent=4))
                    break
    return


if __name__ == '__main__':
    subaccounts_and_metrics_alarm(account_configs)