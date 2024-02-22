import os, json

class ConfigHandler:
    CONFIG_FILE = "/home/evolmonster/InkyWeatherStation/config/config.json"

    def __init__(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as data:
                self.__dict__ = json.loads(data.read())
        else:
            print("Config file not loaded")
    
    def getConfig(self):
        return self.__dict__