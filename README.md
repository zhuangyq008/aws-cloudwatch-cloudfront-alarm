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