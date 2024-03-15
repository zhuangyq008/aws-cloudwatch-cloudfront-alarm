# account_configs.py
from ddb_account_metric_config_items import DdbAccountMetricConfigItems
"""

Args:
    account_configs (list): A list of dictionaries containing configuration for each account.
        Each dictionary should contain the following keys:
        - 'account_id': The AWS account ID.
        - 'assume_role_arn': The ARN of the role to assume when accessing the AWS API.
        - 'period': The period for CloudWatch metrics.
        - 'minutes': The number of minutes to subtract from the current time for metric retrieval.
        - 'threshold': The threshold value for high request metrics.
        - 'consecutive_points': The number of consecutive high points to trigger a notification.

Returns:
    list: A list of dictionaries containing the subaccount ID, name, and metrics.
"""
account_configs = [
    {
        'account_id': '994693907619',
        'account_name': 'm18396314820',
        'role': 'OrganizationAccountAccessRole',
        'period': 300,
        'minutes': 30,
        'threshold': 100,
        'consecutive_points': 2,
        'payer_topic_name': 'metric-alarm-topic',
        'linked_topic_name': 'metric-alarm-topic-1',
        'status': 'enable',
        'send_sns_flag': 'open',
        "send_linked_sns_flag": "close",
        'save_metric_log_flag': 'open'
        # ,'payer_email_addresses' : ['1@163.com', '1@gmail.com']
    },
    # Add more account configurations here if needed
]


metric_table = DdbAccountMetricConfigItems()

# 读取项目
print("\nReading account_configs...")
# account_configs = metric_table.read_item_by_status()
# print("Read account_configs:", account_configs)
