from ddb_dao import DdbDao

class DdbMetricLogItems(DdbDao):
    def __init__(self):
        super().__init__('metric-log-items')
    
    def read_item_by_status(self):
        response = self.query_items_by_attribute('status', 'enable')
        return response
    
# 测试代码
if __name__ == "__main__":
    # 创建一个 DdbAccountMetricConfigItems 实例
    metric_log = DdbMetricLogItems()

