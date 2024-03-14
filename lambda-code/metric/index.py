# index.py
from metric import subaccounts_and_metrics_alarm
from account_configs import account_configs

def handler(event, context):
    metrics_data = subaccounts_and_metrics_alarm(account_configs)
    print(metrics_data)