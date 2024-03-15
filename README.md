# 介绍
AWS CloudFront alarm that the total number of requests within a period of time exceeds the standard
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
└── metric-alarm-stack.ts   采集&告警
└── metric-alarm-stack.ts   写入日志
```