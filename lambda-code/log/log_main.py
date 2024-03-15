from helper_utils import HelperUtils
from ddb_metric_log_items import DdbMetricLogItems

def save_log(sns_message):
    print(f'sns_message: {sns_message[:30]}')
    json_obj = HelperUtils.parse_formatted_text(sns_message)
    print(f'prepare save log')
    # print(json_obj)
    metric_log = DdbMetricLogItems()
    metric_log.create_item(json_obj)
    return json_obj


if __name__ == '__main__':
    sns_message='''
- name: High request metrics for account: 12323, distribution id: E3QAV0KAZ77VW2,
- description: 请查看cloudfront分发监控，确认您的流量是否存在异常
- state_change: OK -> ALARM
- reason_for_state_change: OK -> ALARM: 连续1次在5.0分钟时间段的总请求数列表为： 125.0，均超过设定的阈值: 100. 
- timestamp: 2024-03-15 06:12:00
- alarm_id: '1232'
- aws_account: 12323
- alarm_arn: None
- datapoints:
- threshold:
    - metric_name: Requests
    - metric_namespace: AWS/CloudFront
    - period: 300
    - extended_statistic: Sum
    - unit: None
    - threshold: 100
    - comparison_operator: GreaterThanThreshold
    - evaluation_periods: 1
- state_change_actions:
    - Action1: Send ALARM
    - Action2: Save ALARM Log
   '''
    json_message = save_log(sns_message)
    print(json_message)