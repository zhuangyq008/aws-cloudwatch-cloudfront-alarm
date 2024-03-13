import boto3

def get_sns():
    sns_client = boto3.client('sns')
    return sns_client

def check_topic_existence(topic_name):
    sns_client = get_sns()
    response = sns_client.list_topics()
    topics = response['Topics']
    for topic in topics:
        if topic_name in topic['TopicArn']:
            return topic['TopicArn']  # 如果主题已存在，返回现有主题的 ARN
    return None

def create_topic(topic_name):
    existing_topic_arn = check_topic_existence(topic_name)
    if existing_topic_arn:
        print("Topic already exists with ARN:", existing_topic_arn)
        return existing_topic_arn
    else:
        sns_client = get_sns()
        response = sns_client.create_topic(Name=topic_name)
        return response['TopicArn']

def check_subscription_existence(topic_arn, email_address):
    sns_client = get_sns()
    response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    subscriptions = response['Subscriptions']
    for subscription in subscriptions:
        if subscription['Protocol'] == 'email' and subscription['Endpoint'] == email_address:
            return True
    return False

def subscribe_email_to_topic(topic_arn, email_address):
    if not check_subscription_existence(topic_arn, email_address):
        sns_client = get_sns()
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_address
        )
        return response['SubscriptionArn']
    else:
        print("Email address already subscribed to the topic.")
        return None

# TODO: 需要处理短时间的重复发送
def publish_message_to_topic(topic_arn, message):
    if topic_arn:
        # 发布消息到 SNS 主题
        sns_client = get_sns()
        response = sns_client.publish(
            TopicArn=topic_arn,
            Subject='cdn request over limit',
            Message=message
            # MessageAttributes={
            #     'email': {
            #         'DataType': 'String.Array',
            #         'StringValue': ','.join(email_addresses)
            #     }
            # }
        )
        print(f"Message published successfully.Message: {message}")

