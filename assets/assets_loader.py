from PyQt6.QtCore import QDir
from PyQt6.QtWidgets import QWidget
from PyQt6.uic import load_ui
import os

class Assets:

    @staticmethod
    def getAssetsPath(dirName = ""):
        return os.path.join(QDir.currentPath(),  'assets', dirName)


    @staticmethod
    def loadQss(name:str, qtinstance):
        path = os.path.join(Assets.getAssetsPath('qss'), name + '.qss')
        res = ""
        with open(path, 'r', encoding='utf8') as f:
            res = f.read()
        if res:
            qtinstance.setStyleSheet(res)
    
    @staticmethod
    def loadUi(name:str, qtinstance):
        path = os.path.join(Assets.getAssetsPath('ui'), name + '.ui')
        load_ui.loadUi(path, qtinstance)