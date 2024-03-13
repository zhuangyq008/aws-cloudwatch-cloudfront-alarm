# metric-alarm
AWS CloudFront alarm that the total number of requests within a period of time exceeds the standard
## 首次部署
### 构建CDK应用程序
```
# compile typescript to js, 这个步骤可选
# 部署时候，cdk也会自动build
npm run build
```
### cdk bootstrap
cdk bootstrap, 这个cdk引导工作只需要做一次
```
# 指定aws cli的profile和区域
export AWS_PROFILE=sandbox
export AWS_DEFAULT_REGION=us-west-2
# bootstrap会关联aws账户和区域，并在aws上生成一个CDK Tookie堆栈
cdk bootstrap
# 或者指定profile
# cdk bootstrap --profile sandbox --region us-west-2
```
### cdk synth(可选)
```
# 可选，输出CloudFormation模版文件
cdk synth
# 把输出yaml内容保存到文件
# cdk synth > metric-alarm.template.yaml
```
### 部署CDK应用程序
```
# 部署堆栈AWS CloudFormation到aws账户
cdk deploy
```
## 二次部署
修改lambda代码或者cdk代码后
```
cdk deploy
```
# 代码
## lambda代码
```
lambda-code/
    └── metric                 采集&告警的lambda
        ├── index.py           lambda主函数
        ├── metric.py          业务逻辑主体：采集指标、告警
        ├── sns_main.py        sns主函数：判断如果有payer的告警主题，则发布消息
        └── sns_operations.py  sns创建主题，订阅主题，发布主题的函数
```
## CDK代码
```
lib
└── metric-alarm-stack.ts   采集&告警
```