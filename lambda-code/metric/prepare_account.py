import boto3
from ddb_account_metric_config_items import DdbAccountMetricConfigItems

def get_subaccounts():

  # Get a list of all sub-accounts for the AWS root account
  org = boto3.client('organizations')
  response = org.list_accounts()
  accounts = response['Accounts']
#   print(f"Metrics for account {accounts}")
  # Loop through each sub-account  
  for account in accounts:
    # Get the account ID
    print(f"Metrics for account {account['Id']} {account['Name']}")
  return accounts

def construct_account(account):
    # 构造包含所需信息的字典对象
    metrics_object = {
        "account_id": account['Id'],
        "role": "OrganizationAccountAccessRole",
        "account_name": account['Name'],
        "consecutive_points": 3,
        "minutes": 30,
        "payer_topic_name": "metric-alarm-topic",
        "period": 300,
        "save_metric_log_flag": "open",
        "send_sns_flag": "open",
        "status": "disable",
        "threshold": 5000
    }
    return metrics_object

def writeDb(account):
    account_item = construct_account(account)
    metric_table = DdbAccountMetricConfigItems()
    response = metric_table.create_item(account_item)
    return response

def write(accounts):
   for account in accounts:
      writeDb(account)
   
if __name__ == '__main__':
    accounts = get_subaccounts()
    write(accounts)
