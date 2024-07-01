import json

class Config:
    def __init__(self):
        pass
    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    
    def save_config(self, config, config_path):
        with open(config_path, 'w') as f:
            json.dump(config, f, indent = 4)