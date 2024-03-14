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

        # List all CloudFront distributions
        distributions = list_deployed_distributions(assumed_role_credentials)

        for distribution in distributions:
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
                        'Datapoints': metric_statistics['Datapoints']
                    })
                else:
                    consecutive_high_points = 0
                    all_metrics = []

                print(f"consecutive_high_points： {consecutive_high_points}")
                if consecutive_high_points >= config['consecutive_points']:
                    print("true")
                    # TODO: 需要判断发送过后，多少分钟再次发


    return all_metrics


if __name__ == '__main__':
    metrics_data = subaccounts_and_metrics_alarm(account_configs)
    print(metrics_data)