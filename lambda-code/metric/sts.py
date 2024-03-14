# aws.py
import boto3

def get_assumed_role_credentials(role_arn):
    sts_client = boto3.client('sts')
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='AssumeRoleSession1'
    )
    return assumed_role_object['Credentials']
