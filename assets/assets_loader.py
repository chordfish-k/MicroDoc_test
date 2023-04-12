from PySide6.QtCore import QDir, QFile
from PySide6.QtWidgets import QWidget, QMainWindow
from PySide6.QtUiTools import loadUiType, QUiLoader

import os

from util.logger import logger


class Assets:

    @staticmethod
    def getAssetsPath(dirName = ""):
        return os.path.join(QDir.currentPath(),  'assets', dirName)


    #@staticmethod
    #def solveQssVar(name:str, )


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
        
        qtinstance.ui = loadUiType(path)[0]()
        if qtinstance.ui:
            logger.debug("loaded uifile succeed: " + path)
            qtinstance.ui.setupUi(qtinstance)
        else:
            logger.warning("loaded uifile failed: " + path)