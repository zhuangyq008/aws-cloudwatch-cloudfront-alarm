# introduce
AWS CloudFront alarm that the total number of requests within a period of time exceeds the standard
This project will create
* Cloud Watch EventBridge
*Two Lambda Function
*Two DynamoDB Table

Please run `cdk deploy --all` to deploy this stack in your AWS account.
# deploy
## Manually create SNS, TOPIC is consistent with the configuration data
## Deploy CDK application
```
cdk deploy --all
```
## Set up Linked Account
Configuration data is saved in DynamoDB

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