# introduce [[中文](README_cn.md)]

AWS CloudFront alarm that the total number of requests within a period of time exceeds the standard

Please run `cdk deploy --all` to deploy this stack in your AWS account.

# deploy

## 1.Deploy CDK application

```
cdk deploy --all
```

This project will create

* Cloud Watch EventBridge
* Two Lambda Function
* Two DynamoDB Table

## 2.Manually create SNS

![SNS Infomation](docs/images/sns_detail.png)

Note:

- TOPIC Name of sns must be consistent with the following topic configuration data
- Creating a subscription can also be set in the final step.

## 3.Set up The configuration data for Linked Account in the DynamoDB Table

table name: account-metric-config-items

Example Record:

```
{
 "account_id": "11111",
 "account_name": "testaccount",
 "consecutive_points": 4,
 "linked_topic_name": "metric-alarm-topic-zhangzhongyun",
 "minutes": 30,
 "payer_topic_name": "metric-alarm-topic",
 "period": 300,
 "role": "testrole",
 "save_metric_log_flag": "open",
 "send_linked_sns_flag": "close",
 "send_sns_flag": "open",
 "status": "enable",
 "threshold": 2000
}
```

![config list](docs/images/config_list.png)
![config detail](docs/images/config_detail.png)

Note:

- You can write a program to read all accounts under payer and write them automatically
- You can write a program to automatically create sns based on configuration
- payer_topic_name must be the same as the sns topic created in step 1
- All LinkedAccount alerts will be sent to payer_topic_name
- If send_linked_sns_flag is open, you need to create a LinkedAccount sns. The topic must be the same as linked_topic_name. This only sends alarms under this account.

# code

## lambda code

```
lambda-code/
     └── metric collection & alarm lambda
         ├── index.py lambda main function
         ├── metric.py business logic body: collecting indicators and alarms
```

## Code debugging

It is recommended to run python directly

```
Modify input parameters, run metric.py, etc.
```

## CDK code

```
lib
└── metric-alarm-stack.ts reads configuration, collects indicators, and alarms
└── metric-alarm-stack.ts writes alarm log
```
