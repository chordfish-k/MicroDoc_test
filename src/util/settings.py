from PySide6.QtCore import QDir
from configparser import ConfigParser
from src.util.logger import logger
from src.util.share import ObjectManager
import os

setting_path = os.path.join(QDir.currentPath(), "settings.ini")


class Settings:
    config = ConfigParser()
    config_dict: dict = {}
    file_path: str = setting_path

    def __init__(self, file_path: str = setting_path):
        self.file_path = file_path
        self.load()

        if not self.config.has_section('settings'):
            self.config.add_section('settings')

    def setItem(self, key: str, value):
        self.config_dict[key] = value

    def deleteItem(self, key: str):
        self.config_dict.pop(key)

    def setItemIfNone(self, key: str, value):
        if not self.config_dict.get(key):
            self.config_dict[key] = value

    def get(self, key: str, value_type: type = str):
        if value_type is bool:
            return True if self.config_dict.get(key) == 'True' else False
        if self.config_dict.get(key):
            return value_type(self.config_dict.get(key))
        else:
            return None

    def load(self):
        self.config.read(self.file_path, encoding='gbk')
        self.config_dict.clear()
        for item in self.config.items('settings'):
            self.config_dict[item[0]] = item[1]

    def save(self):
        if self.file_path:
            for key in self.config_dict:
                self.config.set('settings', key, self.config_dict[key])
            self.config.write(open(self.file_path, 'w'))
        else:
            logger.warning("没有指定设置文件名")


settings = Settings()
ObjectManager.set("settings", settings)

# 设置logger可输出日志级别范围
logger.setLevel(settings.get("logger_level"))
