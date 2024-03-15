# index.py
import json
from log_main import save_log

def handler(event, context):
    # 检查事件是否来自 SNS
    if 'Records' in event and len(event['Records']) > 0:
        # 解析 SNS 消息
        sns_message = json.loads(event['Records'][0]['Sns']['Message'])
        
        # 在这里处理 SNS 消息
        print("Received SNS message:", sns_message)
        
        # 保存日志或执行其他操作
        save_log(sns_message)
    else:
        return
