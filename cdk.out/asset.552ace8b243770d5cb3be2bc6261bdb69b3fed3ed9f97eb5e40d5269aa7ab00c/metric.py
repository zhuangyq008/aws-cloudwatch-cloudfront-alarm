import datetime
import boto3
import os
from sns.sns_main import run_sns_operations

# Get a list of all subaccounts and their associated metrics.

def get_subaccounts_and_metrics(account_configs):
    """
    Get a list of all subaccounts and their associated metrics.

    Args:
        account_configs (list): A list of dictionaries containing configuration for each account.
            Each dictionary should contain the following keys:
            - 'account_id': The AWS account ID.
            - 'assume_role_arn': The ARN of the role to assume when accessing the AWS API.
            - 'period': The period for CloudWatch metrics.
            - 'minutes': The number of minutes to subtract from the current time for metric retrieval.
            - 'threshold': The threshold value for high request metrics.
            - 'consecutive_points': The number of consecutive high points to trigger a notification.

    Returns:
        list: A list of dictionaries containing the subaccount ID, name, and metrics.
    """

    all_metrics = []

    for config in account_configs:
        account_id = config['account_id']
        assume_role_arn = config['assume_role_arn']
        period = config['period']
        minutes = config['minutes']
        threshold = config['threshold']
        consecutive_points = config['consecutive_points']
        topic_name = config['topic_name']
        email_addresses = config['email_addresses']

        # Create an STS client
        sts_client = boto3.client('sts')

        # Assume the role
        assumed_role_object = sts_client.assume_role(
            RoleArn=assume_role_arn,
            RoleSessionName='AssumeRoleSession1'
        )
        credentials = assumed_role_object['Credentials']
        aws_access_key_id = credentials['AccessKeyId']
        aws_secret_access_key = credentials['SecretAccessKey']
        aws_session_token = credentials['SessionToken']

        # Initialize CloudWatch client
        cloudwatch = boto3.client('cloudwatch',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  aws_session_token=aws_session_token, region_name='us-east-1')

        # List all CloudFront distributions and obtain the last half-hour request metrics data from CloudWatch
        cloudfront = boto3.client('cloudfront',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  aws_session_token=aws_session_token)
        distributions = cloudfront.list_distributions()
        for distribution in distributions['DistributionList']['Items']:
            # When the status is available
            if distribution['Status'] == 'Deployed':
                distribution_id = distribution['Id']
                print(f"Metrics for cdn {distribution_id}")
                metrics = cloudwatch.list_metrics(Namespace='AWS/CloudFront',
                                                  Dimensions=[{'Name': 'DistributionId', 'Value': distribution_id}])
                for metric in metrics['Metrics']:
                    if metric['MetricName'] == 'Requests':
                        # Subtract minutes from the current UTC time
                        start_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes)

                        # Add 8 hours to the current UTC time
                        end_time = datetime.datetime.utcnow()
                        print(f"Metrics for cdn start_time: {start_time} end_time: {end_time}")
                        metric_statistics = cloudwatch.get_metric_statistics(
                            MetricName='Requests',
                            Namespace='AWS/CloudFront',
                            StartTime=start_time,
                            EndTime=end_time,
                            Period=period,
                            Statistics=['Sum'],
                            Dimensions=[{'Name': 'DistributionId', 'Value': distribution_id},
                                        {'Name': 'Region', 'Value': 'Global'}]
                        )
                        print(f"Metrics for cdn {metric_statistics}")
                        consecutive_high_points = 0
                        for point in metric_statistics['Datapoints']:
                            # If the values of consecutive_points consecutive data points in the loop are all greater than or equal to threshold,
                            # then send a message to SNS
                            if point['Sum'] >= threshold:
                                consecutive_high_points += 1
                            else:
                                consecutive_high_points = 0

                            if consecutive_high_points >= consecutive_points:
                                # Send SNS message here

                                # 在linkedAccount上发送告警
                                # sns = boto3.client('sns',
                                #                     aws_access_key_id=aws_access_key_id,
                                #                     aws_secret_access_key=aws_secret_access_key,
                                #                     aws_session_token=aws_session_token)

                                # 在payer账号发送告警
                                message = f"High request metrics for {distribution_id}"
                                run_sns_operations(topic_name, email_addresses, message)
                                # TODO: 需要判断发送过后，多少分钟再次发送
                        consecutive_high_points = 0

                        # Append metrics to the list
                        all_metrics.append({
                            'AccountId': account_id,
                            'DistributionId': distribution_id,
                            'StartTime': start_time,
                            'EndTime': end_time,
                            'Metrics': metric_statistics
                        })

    return all_metrics


if __name__ == '__main__':
    account_configs = [
        {
            'account_id': '611234940057',
            'assume_role_arn': 'arn:aws:iam::611234940057:role/OrganizationAccountAccessRole',
            'period': 300,
            'minutes': 180,
            'threshold': 10,
            'consecutive_points': 3,
            'topic_name' : 'metric-alarm-topic',
            'email_addresses' : ['jarrywen@163.com', 'jarrywenjack@gmail.com']
        },
        # Add more account configurations here if needed
    ]
    metrics_data = get_subaccounts_and_metrics(account_configs)
    print(metrics_data)