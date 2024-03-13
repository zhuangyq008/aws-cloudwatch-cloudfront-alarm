"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MetricAlarmStack = void 0;
const cdk = require("aws-cdk-lib");
const lambda = require("aws-cdk-lib/aws-lambda");
const events = require("aws-cdk-lib/aws-events");
const targets = require("aws-cdk-lib/aws-events-targets");
class MetricAlarmStack extends cdk.Stack {
    constructor(scope, id, props) {
        super(scope, id, props);
        // 创建 Python Lambda 函数
        const pythonLambda = new lambda.Function(this, 'MyPythonLambda', {
            runtime: lambda.Runtime.PYTHON_3_8,
            handler: 'index.handler', // 指定 Lambda 处理程序的入口函数
            code: lambda.Code.fromAsset('./lambda-code/metric'), // 替换为您的 Python Lambda 代码路径
        });
        // 创建定时触发器，每天执行一次
        // const rule = new events.Rule(this, 'MyRule', {
        //   schedule: events.Schedule.cron({ minute: '0', hour: '1' }), // 每天凌晨 1 点执行
        // });
        // 创建定时触发器，每5分钟执行一次
        const rule = new events.Rule(this, 'MyRule', {
            schedule: events.Schedule.rate(cdk.Duration.minutes(1)), // 每5分钟执行一次
        });
        rule.addTarget(new targets.LambdaFunction(pythonLambda));
    }
}
exports.MetricAlarmStack = MetricAlarmStack;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibWV0cmljLWFsYXJtLXN0YWNrLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsibWV0cmljLWFsYXJtLXN0YWNrLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7OztBQUFBLG1DQUFtQztBQUVuQyxpREFBaUQ7QUFDakQsaURBQWlEO0FBQ2pELDBEQUEwRDtBQUUxRCxNQUFhLGdCQUFpQixTQUFRLEdBQUcsQ0FBQyxLQUFLO0lBQzdDLFlBQVksS0FBZ0IsRUFBRSxFQUFVLEVBQUUsS0FBc0I7UUFDOUQsS0FBSyxDQUFDLEtBQUssRUFBRSxFQUFFLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFFeEIsc0JBQXNCO1FBQ3RCLE1BQU0sWUFBWSxHQUFHLElBQUksTUFBTSxDQUFDLFFBQVEsQ0FBQyxJQUFJLEVBQUUsZ0JBQWdCLEVBQUU7WUFDL0QsT0FBTyxFQUFFLE1BQU0sQ0FBQyxPQUFPLENBQUMsVUFBVTtZQUNsQyxPQUFPLEVBQUUsZUFBZSxFQUFFLHNCQUFzQjtZQUNoRCxJQUFJLEVBQUUsTUFBTSxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsc0JBQXNCLENBQUMsRUFBRSwyQkFBMkI7U0FDakYsQ0FBQyxDQUFDO1FBRUgsaUJBQWlCO1FBQ2pCLGlEQUFpRDtRQUNqRCw4RUFBOEU7UUFDOUUsTUFBTTtRQUNOLG1CQUFtQjtRQUNuQixNQUFNLElBQUksR0FBRyxJQUFJLE1BQU0sQ0FBQyxJQUFJLENBQUMsSUFBSSxFQUFFLFFBQVEsRUFBRTtZQUMzQyxRQUFRLEVBQUUsTUFBTSxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUFDLENBQUMsRUFBRSxXQUFXO1NBQ3JFLENBQUMsQ0FBQztRQUNILElBQUksQ0FBQyxTQUFTLENBQUMsSUFBSSxPQUFPLENBQUMsY0FBYyxDQUFDLFlBQVksQ0FBQyxDQUFDLENBQUM7SUFDM0QsQ0FBQztDQUNGO0FBckJELDRDQXFCQyIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIGNkayBmcm9tICdhd3MtY2RrLWxpYic7XG5pbXBvcnQgeyBDb25zdHJ1Y3QgfSBmcm9tICdjb25zdHJ1Y3RzJztcbmltcG9ydCAqIGFzIGxhbWJkYSBmcm9tICdhd3MtY2RrLWxpYi9hd3MtbGFtYmRhJztcbmltcG9ydCAqIGFzIGV2ZW50cyBmcm9tICdhd3MtY2RrLWxpYi9hd3MtZXZlbnRzJztcbmltcG9ydCAqIGFzIHRhcmdldHMgZnJvbSAnYXdzLWNkay1saWIvYXdzLWV2ZW50cy10YXJnZXRzJztcblxuZXhwb3J0IGNsYXNzIE1ldHJpY0FsYXJtU3RhY2sgZXh0ZW5kcyBjZGsuU3RhY2sge1xuICBjb25zdHJ1Y3RvcihzY29wZTogQ29uc3RydWN0LCBpZDogc3RyaW5nLCBwcm9wcz86IGNkay5TdGFja1Byb3BzKSB7XG4gICAgc3VwZXIoc2NvcGUsIGlkLCBwcm9wcyk7XG5cbiAgICAvLyDliJvlu7ogUHl0aG9uIExhbWJkYSDlh73mlbBcbiAgICBjb25zdCBweXRob25MYW1iZGEgPSBuZXcgbGFtYmRhLkZ1bmN0aW9uKHRoaXMsICdNeVB5dGhvbkxhbWJkYScsIHtcbiAgICAgIHJ1bnRpbWU6IGxhbWJkYS5SdW50aW1lLlBZVEhPTl8zXzgsXG4gICAgICBoYW5kbGVyOiAnaW5kZXguaGFuZGxlcicsIC8vIOaMh+WumiBMYW1iZGEg5aSE55CG56iL5bqP55qE5YWl5Y+j5Ye95pWwXG4gICAgICBjb2RlOiBsYW1iZGEuQ29kZS5mcm9tQXNzZXQoJy4vbGFtYmRhLWNvZGUvbWV0cmljJyksIC8vIOabv+aNouS4uuaCqOeahCBQeXRob24gTGFtYmRhIOS7o+eggei3r+W+hFxuICAgIH0pO1xuXG4gICAgLy8g5Yib5bu65a6a5pe26Kem5Y+R5Zmo77yM5q+P5aSp5omn6KGM5LiA5qyhXG4gICAgLy8gY29uc3QgcnVsZSA9IG5ldyBldmVudHMuUnVsZSh0aGlzLCAnTXlSdWxlJywge1xuICAgIC8vICAgc2NoZWR1bGU6IGV2ZW50cy5TY2hlZHVsZS5jcm9uKHsgbWludXRlOiAnMCcsIGhvdXI6ICcxJyB9KSwgLy8g5q+P5aSp5YeM5pmoIDEg54K55omn6KGMXG4gICAgLy8gfSk7XG4gICAgLy8g5Yib5bu65a6a5pe26Kem5Y+R5Zmo77yM5q+PNeWIhumSn+aJp+ihjOS4gOasoVxuICAgIGNvbnN0IHJ1bGUgPSBuZXcgZXZlbnRzLlJ1bGUodGhpcywgJ015UnVsZScsIHtcbiAgICAgIHNjaGVkdWxlOiBldmVudHMuU2NoZWR1bGUucmF0ZShjZGsuRHVyYXRpb24ubWludXRlcygxKSksIC8vIOavjzXliIbpkp/miafooYzkuIDmrKFcbiAgICB9KTtcbiAgICBydWxlLmFkZFRhcmdldChuZXcgdGFyZ2V0cy5MYW1iZGFGdW5jdGlvbihweXRob25MYW1iZGEpKTtcbiAgfVxufVxuIl19