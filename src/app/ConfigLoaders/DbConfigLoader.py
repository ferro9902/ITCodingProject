import json


# DB connection configuration parameters loader

class DbConfigLoader:

    def __init__(self):
        config_file = "src\\resources\\db_config.json"
        self.config = DbConfigLoader.load_config(config_file)

    def load_config(file_path: str):
        with open(file_path, "r") as file:
            config = json.load(file)
        return config

    def get_param(self, field_name: str):
        return self.config[field_name]
