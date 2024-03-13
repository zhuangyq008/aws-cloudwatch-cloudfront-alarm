import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';

export class MetricAlarmStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // 创建 Python Lambda 函数
    const pythonLambda = new lambda.Function(this, 'MyPythonLambda', {
      runtime: lambda.Runtime.PYTHON_3_8,
      handler: 'index.handler', // 指定 Lambda 处理程序的入口函数
      code: lambda.Code.fromAsset('path/to/python-lambda-code'), // 替换为您的 Python Lambda 代码路径
    });

    // 创建定时触发器，每天执行一次
    const rule = new events.Rule(this, 'MyRule', {
      schedule: events.Schedule.cron({ minute: '0', hour: '1' }), // 每天凌晨 1 点执行
    });
    rule.addTarget(new targets.LambdaFunction(pythonLambda));
  }
  }
}
