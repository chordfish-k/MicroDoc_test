from configparser import ConfigParser
from util.logger import logger

class Settings:
    config = ConfigParser()
    config_dict:dict = {}
    file_path:str = "./settings.ini"

    def __init__(self, file_path:str = "./settings.ini"):
        self.file_path = file_path
        
        if not self.config.has_section('settings'):
            self.config.add_section('settings')

    
    def setItem(self, key:str, value):
        self.config_dict[key] = value

    def get(self, key:str):
        return self.config_dict.get(key)


    def load(self):
        self.config.read(self.file_path)
        self.config_dict.clear()
        for item in self.config.items('settings'):
            self.config_dict.append({item[0]: item[1]})


    def save(self):
        if self.file_path:
            for key in self.config_dict:
                self.config.set('settings', key, self.config_dict[key])
            self.config.write(open(self.file_path, 'w'))
        else:
            logger.warning("没有指定设置文件名")

