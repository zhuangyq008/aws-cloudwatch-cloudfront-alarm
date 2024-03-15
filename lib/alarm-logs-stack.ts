import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam'; // 引入 IAM 相关模块
import * as ddb from 'aws-cdk-lib/aws-dynamodb';

export class AlarmLogsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);


    //crate a dynamodb table
    const table = new ddb.Table(this, 'MetricLogItemsTable', {
      tableName: 'metric-log-items',
      partitionKey: {name: 'alarm_id', type: ddb.AttributeType.STRING},
      billingMode: ddb.BillingMode.PAY_PER_REQUEST,
      // timeToLiveAttribute: 'expire_time', // 定义 TTL 属性名称
      removalPolicy: cdk.RemovalPolicy.DESTROY
    })

    // 创建 Lambda 执行角色并附加策略
    const logLambdaExecutionRole = new iam.Role(this, 'LambdaExecutionRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'), // Lambda 服务的身份标识
    });

    // 为 Lambda 执行角色添加策略
    logLambdaExecutionRole.addToPolicy(new iam.PolicyStatement({
      actions: ['logs:CreateLogGroup', 'logs:CreateLogStream', 'logs:PutLogEvents'],
      resources: ['*'], // 允许 Lambda 写入 CloudWatch Logs
    }));

    // 为 Lambda 执行角色添加所有 SNS 权限
    logLambdaExecutionRole.addToPolicy(new iam.PolicyStatement({
      actions: [
        'sns:Receive'
      ],
      resources: ['*'], // 这里资源可以根据你的实际需求进行限制
    }));

    // 添加 Lambda 执行 DynamoDB 操作的权限
    table.grantWriteData(logLambdaExecutionRole);


    // 创建 Python Lambda 函数
    const logLambda = new lambda.Function(this, 'MetricLambda', {
      runtime: lambda.Runtime.PYTHON_3_8,
      handler: 'index.handler', // 指定 Lambda 处理程序的入口函数
      code: lambda.Code.fromAsset('./lambda-code/log'), // 替换为您的 Python Lambda 代码路径
      role: logLambdaExecutionRole, // 关联 Lambda 执行角色
      memorySize: 128, // 内存128M
      timeout: cdk.Duration.minutes(1) // 设置超时时间为 3 分钟
    });

  }
}
