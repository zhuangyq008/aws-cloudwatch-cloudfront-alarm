from ddb_manager import DynamoDBManager

class DdbMetricAccountConfigItems(DynamoDBManager):
    def __init__(self):
        super().__init__('metric_account_config_items')

# 测试代码
if __name__ == "__main__":
    # 创建一个 MetricAccountConfigItems 实例
    metric_table = DdbMetricAccountConfigItems()

    # 测试数据
    test_item = {
        'account_id': '611234940057',
        'role': 'OrganizationAccountAccessRole',
        'assume_role_arn': '',
        'period': 300,
        'minutes': 30,
        'threshold': 10,
        'consecutive_points': 3,
        'payer_topic_name': 'metric-alarm-topic',
        'status': 'enable',
        'send_sns_flag': 'open',
        'save_metric_log_flag': 'open'
    }

    # 创建项目
    print("Creating item...")
    response = metric_table.create_item(test_item)
    print("Create item response:", response)

    # 读取项目
    print("\nReading item...")
    key = {'account_id': '611234940057', 'role': 'OrganizationAccountAccessRole'}
    item = metric_table.read_item(key)
    print("Read item:", item)

    # 更新项目
    print("\nUpdating item...")
    update_expression = "SET minutes = :m"
    expression_attribute_values = {':m': 60}
    response = metric_table.update_item(key, update_expression, expression_attribute_values)
    print("Update item response:", response)

    # 读取更新后的项目
    print("\nReading updated item...")
    item = metric_table.read_item(key)
    print("Updated item:", item)

    # 删除项目
    print("\nDeleting item...")
    response = metric_table.delete_item(key)
    print("Delete item response:", response)
