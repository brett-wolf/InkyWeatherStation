import os, json

class ConfigHandler:
    CONFIG_FILE = "./config.json"

    def __init__(self):
        if os.path.exists(self.CONFIG_FILE):
            print("Loading config file")
            self.__dict__ = json.load(open(self.CONFIG_FILE))
        else:
            print("Config file not loaded")