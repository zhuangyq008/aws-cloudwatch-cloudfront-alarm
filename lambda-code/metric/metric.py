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

                    alarm = Alarm()
                    alarm.name = (
                        f"High request metrics for account: {config['account_id']}, "
                        f"distribution id: {distribution['Id']},"
                    )
                    alarm.description = "请查看cloudfront分发监控，确认您的流量是否存在异常"

                    # 假设 point['Timestamp'] 是一个 datetime 对象
                    point_timestamp = point['Timestamp']
                    # 获取毫秒部分
                    milliseconds = point_timestamp.microsecond // 1000
                    # 格式化日期和时间，包含毫秒
                    formatted_datetime = point_timestamp.strftime("%Y%m%d%H%M%S") + f"{milliseconds:03d}"
                    alarm.alarm_id = config['account_id']+"-"+formatted_datetime
                    alarm.aws_account = config['account_id']
                    alarm.timestamp = point_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    alarm.state_change = "OK -> ALARM"
                    alarm.reason_for_state_change =(
                        f"OK -> ALARM: "
                        f"连续{config['consecutive_points']}次在{config['period']/60}分钟时间段的总请求数列表为： {sum_str}，"
                        f"均超过设定的阈值: {config['threshold']}. "
                    )
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
                    sns_message = HelperUtils.convert_json_text(alarm.__dict__)
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