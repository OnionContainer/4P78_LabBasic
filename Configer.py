import json


class Configer:
    def __init__(self, file_path):

        self.__config_data = self.__read_config(file_path)

    def __read_config(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)  # 将 JSON 转为字典
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error reading config file: {e}")

    def get(self, key):

        return self.__config_data.get(key)

    def get_all(self):

        return self.__config_data

configer = Configer("config.json")
"""
This is a global variable.
configer is readonly.
"""