import os, json

class ConfigHandler(object):
    CONFIG_FILE = "/config.json"

    def __init__(self,screen):
        self.screen = screen

    def read_config(self,opts):
        config_file = ConfigHandler.CONFIG_FILE

        if os.path.exists(config_file):
            with open(config_file,"r") as f:
                opts.update(json.load(f))
    
    def set_options(self,opts):
        self.opts = opts