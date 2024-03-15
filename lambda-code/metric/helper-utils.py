class HelperUtils:
    @staticmethod
    def format_json_string(json_obj, indent=0):
        formatted_str = ""
        for key, value in json_obj.items():
            if isinstance(value, dict):
                formatted_str += "  " * indent + f"- {key}:\n"
                formatted_str += HelperUtils.format_json_string(value, indent + 1)
            else:
                formatted_str += "  " * indent + f"- {key}: {value}\n"
        return formatted_str
    @staticmethod
    def parse_formatted_string(formatted_string):
        json_obj = {}
        current_dict = json_obj
        lines = formatted_string.split('\n')
        for line in lines:
            if line.strip():  # 跳过空行
                key_value_pair = line.strip().split(':')
                key = key_value_pair[0].strip().replace("-", "")  # 移除前导的 "-"
                value = key_value_pair[1].strip()
                if key.endswith(":"):  # 如果是一个新的子对象
                    new_dict = {}
                    current_dict[key[:-1]] = new_dict
                    current_dict = new_dict
                else:
                    current_dict[key] = value
        return json_obj

# # 格式化后的字符串
# formatted_string = """
# - key1: value1
# - key2:
#     - nested_key: nested_value
# """

# # 将格式化后的字符串转换为 JSON 对象
# json_obj = parse_formatted_string(formatted_string)

# # 打印转换后的 JSON 对象
# print(json_obj)