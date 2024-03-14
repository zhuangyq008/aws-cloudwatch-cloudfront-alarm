# cloudfront.py
import boto3

def list_deployed_distributions(credentials):
    cloudfront = boto3.client('cloudfront',
                              aws_access_key_id=credentials['AccessKeyId'],
                              aws_secret_access_key=credentials['SecretAccessKey'],
                              aws_session_token=credentials['SessionToken'])

    distributions = cloudfront.list_distributions()
    return [d for d in distributions['DistributionList']['Items'] if d['Status'] == 'Deployed']
