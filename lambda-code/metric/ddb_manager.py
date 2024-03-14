import boto3

class DynamoDBManager:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def create_item(self, item):
        response = self.table.put_item(Item=item)
        return response

    def read_item(self, key):
        response = self.table.get_item(Key=key)
        return response.get('Item')

    def update_item(self, key, update_expression, expression_attribute_values):
        response = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response

    def delete_item(self, key):
        response = self.table.delete_item(Key=key)
        return response
