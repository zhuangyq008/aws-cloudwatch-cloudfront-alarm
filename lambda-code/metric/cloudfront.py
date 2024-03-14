# cloudfront.py
import boto3

def list_deployed_distributions(credentials):
    cloudfront = boto3.client('cloudfront',
                              aws_access_key_id=credentials['AccessKeyId'],
                              aws_secret_access_key=credentials['SecretAccessKey'],
                              aws_session_token=credentials['SessionToken'])

    distributions = cloudfront.list_distributions()
    # 检查 distributions 字典中是否包含 DistributionList 键以及其下的 Items 键
    if 'DistributionList' in distributions and 'Items' in distributions['DistributionList']:
        return [d for d in distributions['DistributionList']['Items'] if d['Status'] == 'Deployed']
    else:
        # 如果 DistributionList 中没有 Items 键，返回一个空列表
        return []
