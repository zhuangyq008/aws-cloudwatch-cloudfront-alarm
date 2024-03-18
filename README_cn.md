# 介绍

AWS Partners服务一些游戏客户，他们面临的日益增多的网络威胁，在有些Cases造成了大额账单导致客户因无法支付账单而逃逸，我们也评估了Partners在面向这些问题的解决方案，尝试使用Prometheus+Grafana 结合Cloudwatch exporter来监控，但是Partner也给出他们在应对众多的Linked Accounts 这个解决方案带来大量的工作量，如要在Grafana针对每个Linked Account分别配置Datasource及Dashboard , 而且配置告警参数也较多，学习成本比较高。所以我们设计此解决方案的主要解决的问题:

1. 关键指标监控和告警
   我们将基于AWS CloudWatch监控关键的网络和应用程序指标，如请求数、下载流量、错误率等。一旦检测到异常，系统将自动触发告警，通过SNS将告警信息发送到指定运维人员。
2. 自动化部署和配置
   通过自动部署降低配置的工作量，我们的解决方案通过CDK及在DDB的账户配置的扩展以最大限度减少人工干预及提高效率

# 方案特点

1. **可扩展性** : 由于使用了无服务器架构(AWS Lambda),该系统可以根据需求自动扩展,无需预先配置或管理基础设施。
2. **跨账户访问** : 通过链接账户和角色代入机制,该系统可以跨多个 AWS 账户监控和管理资源。
3. **集成性** : 该系统集成了多个 AWS 服务,如 DynamoDB、SNS、CloudWatch 等,提供了完整的监控、警报和通知功能。
4. **可靠性** : 使用 AWS 托管服务,可以提高系统的可靠性和可用性。
5. **灵活性** : 该架构可以根据需求进行扩展和自定义,例如添加更多的监控指标、警报规则或通知渠道。
6. **成本效益** : 由于采用无服务器架构,只在需要时消耗资源,可以降低运营成本。

# 架构图

![Architecture](docs/images/architecture.jpg)

这个架构图描述了一个基于 AWS 服务的监控和警报系统。该系统的主要组件和流程如下:

1. **Scheduler** :一个调度器,可能是 AWS Lambda 函数或 Amazon EventBridge 规则,用于定期触发监控任务。
2. **MetricsAlarm** : 一个 AWS Lambda 函数,负责收集和分析指标数据,并根据预定义的阈值生成警报。
3. **DynamoDB** : 一个 Amazon DynamoDB 数据库,用于存储警报配置及报警事件记录。
4. **Record alarm** : 一个组件,可能是另一个 AWS Lambda 函数,用于将生成的警报记录到其他系统或服务中。
5. **SNS** : 一个 Amazon Simple Notification Service (SNS) 主题,用于发送警报通知。
6. **Mail** : 一个电子邮件服务,用于接收 SNS 主题发送的警报通知。
7. **Linked Accounts** : 一个链接账户的概念,允许该系统跨账户访问和管理其他 AWS 资源。
8. **Assume Role** : 一个 AWS Lambda 函数,用于代入链接账户的角色,以获取访问其他账户资源的权限。
9. **CloudWatch** : Amazon CloudWatch 服务,用于收集和监控 AWS 资源的指标数据。
10. **STS** : AWS Security Token Service (STS),用于管理临时安全凭证,支持跨账户访问。

# 部署

## 前置条件

* Node.js 16+
* AWS CDK CLI
* An AWS Account
* Administrator or equivalent privilege

## 1.部署CDK应用程序

```
cdk deploy --all
```

本工程会创建

* Cloud Watch EventBridge
* Two Lambda Function
* Two DynamoDB Table

## 2.手动创建SNS

![SNS Infomation](docs/images/sns_detail.png)
注：

- TOPIC跟下面的配置数据要一致
- 创建订阅也可以在最后步骤再设置

## 3.在DynamoDB设置LinkedAccout的配置数据

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
注：

- 你可以写一个程序，自动获取payer下的所有账号，自动写入到DynamoDB
- 你可以写一个程序，根据配置自动创建sns
- payer_topic_name必须跟步骤1中创建的sns topic一样
- 所有LinkedAccount的告警都会发送到payer_topic_name
- 如果send_linked_sns_flag为open，则需要创建一个LinkedAccount的sns，topic必须跟linked_topic_name一样，这个只发送这个账号下的告警

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
