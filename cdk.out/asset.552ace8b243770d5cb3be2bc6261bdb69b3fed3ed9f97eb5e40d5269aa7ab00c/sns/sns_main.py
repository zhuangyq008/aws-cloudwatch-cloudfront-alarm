from .sns_operations import create_topic, subscribe_email_to_topic, publish_message_to_topic

def run_sns_operations(topic_name=None, email_addresses=None, message=None):
    if not topic_name:
        print("Please provide a topic name.")
        return
    
    # 创建主题
    topic_arn = create_topic(topic_name)
    print("Topic created with ARN:", topic_arn)

    # 如果提供了邮箱地址，则订阅到主题中
    if email_addresses:
        # 订阅邮箱地址到主题
        for email_address in email_addresses:
            subscription_arn = subscribe_email_to_topic(topic_arn, email_address)
            print("Email address", email_address, "subscribed to topic with ARN:", subscription_arn)

    # 发布消息到主题
    if message:
        publish_message_to_topic(topic_arn, message)
    else:
        print("No message provided.")

if __name__ == "__main__":
    # 你可以在此处设置要使用的主题名称、订阅邮箱地址列表和消息内容
    topic_name = 'metric-alarm-topic'
    email_addresses = ['jarrywen@163.com', 'jarrywenjack@gmail.com']
    message = "请求次数超出!"

    run_sns_operations(topic_name, email_addresses, message)
