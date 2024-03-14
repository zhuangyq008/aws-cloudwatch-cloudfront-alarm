# index.py
from metric import subaccounts_and_metrics_alarm
from account_configs import account_configs

def handler(event, context):
    subaccounts_and_metrics_alarm(account_configs)