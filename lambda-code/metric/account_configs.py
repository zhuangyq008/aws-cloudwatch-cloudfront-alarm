# account_configs.py
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
        'account_id': '611234940057',
        'role': 'OrganizationAccountAccessRole',
        'period': 300,
        'minutes': 30,
        'threshold': 10,
        'consecutive_points': 3,
        'payer_topic_name': 'metric-alarm-topic',
        'status': 'enable',
        'send_sns_flag': 'open',
        'save_metric_log_flag': 'open'
        # ,'payer_email_addresses' : ['jarrywen@163.com', 'jarrywenjack@gmail.com']
    },
    # Add more account configurations here if needed
]