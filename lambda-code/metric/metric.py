from account_configs import account_configs
from sts import get_assumed_role_credentials
from cloudfront import list_deployed_distributions
from cloudwatch import get_metric_statistics
from sns_main import run_sns_operations

# Get a list of all subaccounts and their associated metrics.

def subaccounts_and_metrics_alarm(account_configs):
    all_metrics = []

    for config in account_configs:
        assume_role_arn = f'arn:aws:iam::{config["account_id"]}:role/{config["role"]}'
        assumed_role_credentials = get_assumed_role_credentials(assume_role_arn)

        print(f"AccountId {config['account_id']} {config['account_name']}")
        # List all CloudFront distributions
        distributions = list_deployed_distributions(assumed_role_credentials)

        for distribution in distributions:
            print(f"DistributionId {distribution['Id']}")
            metric_statistics = get_metric_statistics(assumed_role_credentials, distribution, config['minutes'], config['period'], 'Sum')
            consecutive_high_points = 0
            all_metrics = []
            for point in metric_statistics['Datapoints']:
                # If the values of consecutive_points consecutive data points in the loop are all greater than or equal to threshold,
                # then send a message to SNS
                if point['Sum'] >= config['threshold']:
                    consecutive_high_points += 1
                    # Append metrics to the list
                    all_metrics.append({
                        'AccountId': config['account_id'],
                        'DistributionId': distribution['Id'],
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

                    message = (
                        f"High request metrics for account: {config['account_id']}, "
                        f"distribution id: {distribution['Id']}, "
                        f"超出阈值的次数: {consecutive_high_points}, "
                        f"请求次阈值: {config['threshold']}, "
                        f"cdn请求次数列表: {sum_str}"
                    )
                    # 在payer账号发送告警
                    if config['send_sns_flag'] and config['send_sns_flag'] == 'open':
                        run_sns_operations(config['payer_topic_name'], message)
                    elif config['send_linked_sns_flag'] and config['send_linked_sns_flag'] == 'open':
                        run_sns_operations(config['linked_topic_name'], message)
                    break
    return


if __name__ == '__main__':
    subaccounts_and_metrics_alarm(account_configs)