import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as iam from 'aws-cdk-lib/aws-iam'; // 引入 IAM 相关模块

export class MetricAlarmStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // 创建 Lambda 执行角色并附加策略
    const lambdaExecutionRole = new iam.Role(this, 'LambdaExecutionRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'), // Lambda 服务的身份标识
    });

    // 为 Lambda 执行角色添加策略
    lambdaExecutionRole.addToPolicy(new iam.PolicyStatement({
      actions: ['logs:CreateLogGroup', 'logs:CreateLogStream', 'logs:PutLogEvents', 'sts:*', 'sns:*'],
      resources: ['*'], // 允许 Lambda 写入 CloudWatch Logs
    }));

    // 为 Lambda 执行角色添加 sts:AssumeRole 权限，允许切换角色
    lambdaExecutionRole.addToPolicy(new iam.PolicyStatement({
      actions: ['sts:*'],
      resources: ['*'], // 允许扮演任何角色
    }));

    // 为 Lambda 执行角色添加所有 SNS 权限
    lambdaExecutionRole.addToPolicy(new iam.PolicyStatement({
      actions: [
        'sns:*'   // 允许执行 SNS 的所有操作
      ],
      resources: ['*'], // 这里资源可以根据你的实际需求进行限制
    }));

    // 创建 Python Lambda 函数
    const pythonLambda = new lambda.Function(this, 'MetricLambda', {
      runtime: lambda.Runtime.PYTHON_3_8,
      handler: 'index.handler', // 指定 Lambda 处理程序的入口函数
      code: lambda.Code.fromAsset('./lambda-code/metric'), // 替换为您的 Python Lambda 代码路径
      role: lambdaExecutionRole, // 关联 Lambda 执行角色
    });

    // 创建定时触发器，每天执行一次
    // const rule = new events.Rule(this, 'MyRule', {
    //   schedule: events.Schedule.cron({ minute: '0', hour: '1' }), // 每天凌晨 1 点执行
    // });
    // 创建定时触发器，每5分钟执行一次
    const rule = new events.Rule(this, 'MyRule', {
      schedule: events.Schedule.rate(cdk.Duration.minutes(5)), // 每5分钟执行一次
    });
    rule.addTarget(new targets.LambdaFunction(pythonLambda));
  }
}
