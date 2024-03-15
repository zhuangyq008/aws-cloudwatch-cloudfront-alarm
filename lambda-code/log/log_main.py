from helper_utils import HelperUtils
from ddb_metric_log_items import DdbMetricLogItems

def save_log(sns_message):
    print(f'sns_message: {sns_message}')
    json_message = HelperUtils.parse_formatted_string(sns_message)
    # metric_log = DdbMetricLogItems()
    # metric_log.create_item(metric_log)
    return json_message


if __name__ == '__main__':
    sns_message='''
       - name: High request metrics for account: 994693907619, distribution id: E2H2BYAOQ1C7WB,
       - description: 请查看cloudfront分发监控，确认您的流量是否存在异常
       - state_change: OK -> ALARM
       - reason_for_state_change: OK -> ALARM: 连续4次在5.0分钟时间段的总请求数列表为： 213.0,390.0，均超过设定的阈值: 100.
       - timestamp: 2024-03-15 03:58:00
       - aws_account: 994693907619
       - alarm_arn: None
       - datapoints: []
       - threshold:
         - metric_name: Requests
         - metric_namespace: AWS/CloudFront
         - period: 300
         - extended_statistic: Sum
         - unit: None
         - threshold: 100
         - comparison_operator: GreaterThanThreshold
         - evaluation_periods: 2
       - state_change_actions:
         - Action1: ALARM
         - Action2: executor-default
   '''
    json_message = save_log(sns_message)
    print(json_message)