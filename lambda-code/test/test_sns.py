import boto3
import json

# 创建 SNS 客户端
sns_client = boto3.client('sns')

# 定义邮件消息
email_message = {
    'default': 'default message',
    'email': json.dumps({
        'subject': 'Test Email Subject',
        'body': 'Test Email Body',
        'attachments': [
            {
                'filename': 'example.txt',
                'data': 'dGVzdCBtZXNzYWdlCg=='  # base64编码的文件内容
            }
        ]
    })
}

# 发送消息到 SNS 主题
response = sns_client.publish(
    TopicArn = 'xxx',
    Message=json.dumps(email_message),
    MessageStructure='json'
)

print(response)
