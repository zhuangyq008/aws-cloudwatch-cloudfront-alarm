import boto3
from boto3.dynamodb.conditions import Attr, Key
# from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal

class DynamoDBManager:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    # def deserialize_item(self, item):
    #     deserializer = TypeDeserializer()
    #     return {k: deserializer.deserialize(v) if isinstance(v, dict) else v for k, v in item.items()}
    def deserialize_item(self, item):
        # deserializer = TypeDeserializer()
        deserialized_item = {}
        for key, value in item.items():
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    if isinstance(nested_value, Decimal):
                        deserialized_item[key] = int(nested_value) if nested_value % 1 == 0 else float(nested_value)
                    else:
                        deserialized_item[key] = nested_value
            elif isinstance(value, Decimal):
                deserialized_item[key] = int(value) if value % 1 == 0 else float(value)
            else:
                deserialized_item[key] = value
        return deserialized_item
    def create_item(self, item):
        response = self.table.put_item(Item=item)
        return response

    def read_item(self, key):
        response = self.table.get_item(Key=key)
        if 'Item' in response:
            return self.deserialize_item(response['Item'])
        else:
            return None
    
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
    def query_items_by_attribute(self, index_name, attribute_name, attribute_value):
        response = self.table.query(
            IndexName=index_name,  # 替换为你创建的索引名称
            KeyConditionExpression=Key(attribute_name).eq(attribute_value)
        )
        items = response['Items']
        return [self.deserialize_item(item) for item in items]
    

    def query_items_by_attribute(self, attribute_name, attribute_value):
        response = self.table.scan(
            FilterExpression=Attr(attribute_name).eq(attribute_value)
        )
        items = response['Items']
        return [self.deserialize_item(item) for item in items]
    

