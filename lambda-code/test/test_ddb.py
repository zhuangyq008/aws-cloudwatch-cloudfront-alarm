import boto3

# 创建 DynamoDB 客户端
dynamodb = boto3.client('dynamodb')

# 定义要插入的数据
test_item = {
    'account_id': {'S': '611234940057'},
    'role': {'S': 'OrganizationAccountAccessRole'},
    'period': {'N': '300'},
    'minutes': {'N': '30'},
    'threshold': {'N': '10'},
    'consecutive_points': {'N': '3'},
    'payer_topic_name': {'S': 'metric-alarm-topic'},
    'status': {'S': 'enable'},
    'send_sns_flag': {'S': 'open'},
    'save_metric_log_flag': {'S': 'open'}
}

# 插入数据到 DynamoDB 表
response = dynamodb.put_item(
    TableName='account-metric-config-items',
    Item=test_item
)

print("PutItem response:", response)
