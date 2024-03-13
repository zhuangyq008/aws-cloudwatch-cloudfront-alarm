# index.py
from metric import subaccounts_and_metrics_alarm

def handler(event, context):
    account_configs = [
        {
            'account_id': '611234940057',
            'assume_role_arn': 'arn:aws:iam::611234940057:role/OrganizationAccountAccessRole',
            'period': 300,
            'minutes': 180,
            'threshold': 1,
            'consecutive_points': 1,
            'payer_topic_name' : 'metric-alarm-topic'
            # ,'payer_email_addresses' : ['jarrywen@163.com', 'jarrywenjack@gmail.com']
        },
        # Add more account configurations here if needed
    ]
    metrics_data = subaccounts_and_metrics_alarm(account_configs)
    print(metrics_data)