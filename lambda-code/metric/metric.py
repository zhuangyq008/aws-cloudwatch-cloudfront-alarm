from account_configs import account_configs
from sts import get_assumed_role_credentials
from cloudfront import list_deployed_distributions
from cloudwatch import get_metric_statistics
from sns_main import run_sns_operations
from alarm import Alarm
from helper_utils import HelperUtils
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

                    # message = (
                    #     f"High request metrics for account: {config['account_id']}, "
                    #     f"distribution id: {distribution['Id']}, "
                    #     f"超出阈值的次数: {consecutive_high_points}, "
                    #     f"请求次阈值: {config['threshold']}, "
                    #     f"cdn请求次数列表: {sum_str}"
                    # )

                    # TODO:根据请求总数超出阈值的倍数来确定告警的等级

                    alarm = Alarm()
                    alarm.name = (
                        f"High request metrics for account: {config['account_id']}, "
                        f"distribution id: {distribution['Id']},"
                    )
                    alarm.description = "请查看cloudfront分发监控，确认您的流量是否存在异常"
                    
                    alarm.aws_account = config['account_id']
                    alarm.timestamp = point['Timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                    alarm.state_change = "OK -> ALARM"
                    # 英文版
                    # alarm.reason_for_state_change = (
                    #     f"OK -> ALARM: "
                    #     f"Total request count for consecutive 4 times in {config['period']/60} minute period: {sum_str}, all exceeding ",
                    #     f"the set threshold: {config['threshold']}. "
                    # )
                    alarm.reason_for_state_change =(
                        f"OK -> ALARM: "
                        f"连续4次在{config['period']/60}分钟时间段的总请求数列表为： {sum_str}，"
                        f"均超过设定的阈值: {config['threshold']}. "
                    )
                    # TypeError: Object of type datetime is not JSON serializable
                    # alarm.datapoints = all_metrics
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
                        "Action1": "Send ALARM",
                        "Action2": "Save ALARM Log" # optional 如禁用资源，可以使用executor-default
                    }
                    sns_message = HelperUtils.format_json_string(alarm.__dict__, indent=4)
                    # sns_message = HelperUtils.format_json_string(json.dumps(alarm.__dict__, indent=4, ensure_ascii=False))
                    print(f"{sns_message}")
                    if config['send_sns_flag'] and config['send_sns_flag'] == 'open':
                        # 在payer账号发送告警
                        run_sns_operations(config['payer_topic_name'], sns_message)
                    elif config['send_linked_sns_flag'] and config['send_linked_sns_flag'] == 'open':
                        run_sns_operations(config['linked_topic_name'], sns_message)
                    break
    return


if __name__ == '__main__':
    subaccounts_and_metrics_alarm(account_configs)