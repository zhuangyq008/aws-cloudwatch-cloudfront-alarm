# 介绍
当CloudFront的Request指标超过设定的阈值的时候，发送告警信息
本工程会创建
* Cloud Watch EventBridge
* Two Lambda Function
* Two DynamoDB Table

Please run `cdk deploy --all` to deploy this stack in your AWS account.
# 部署
## 手动创建SNS，TOPIC跟配置数据一致
## 部署CDK应用程序
```
cdk deploy --all
```
## 设置Linked Account
配置数据保存在DynamoDB

# 代码
## lambda代码
```
lambda-code/
    └── metric                 采集&告警的lambda
        ├── index.py           lambda主函数
        ├── metric.py          业务逻辑主体：采集指标、告警
```
## 代码调试
建议直接运行python
```
修改入参，运行metric.py等
```
## CDK代码
```
lib
└── metric-alarm-stack.ts   读取配置、采集指标、告警
└── metric-alarm-stack.ts   写入告警日志
```