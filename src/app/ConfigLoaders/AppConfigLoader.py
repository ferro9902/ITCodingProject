import json


# application configuration parameters loader

class AppConfigLoader:

    def __init__(self):
        config_file = "src\\resources\\app_config.json"
        self.config = AppConfigLoader.load_config(config_file)

    def load_config(file_path: str):
        with open(file_path, "r") as file:
            config = json.load(file)
        return config

    def get_param(self, field_name: str):
        return self.config[field_name]
