"""
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
            for k in qtinstance.ui.__dict__:
                qtinstance.__dict__[k] = qtinstance.ui.__dict__[k]
        else:
            logger.warning("loaded uifile failed: " + path)


"""
from PySide6.QtCore import QDir, QFile
from PySide6.QtWidgets import QWidget, QMainWindow
from PySide6.QtUiTools import loadUiType, QUiLoader

import os

from util.logger import logger


class Assets:

    globalColors = {}

    uiCache = {}

    @staticmethod
    def getAssetsPath(dirName = ""):
        return os.path.join(QDir.currentPath(),  'assets', dirName)


    @staticmethod
    def loadQdef(name:str):
        path = os.path.join(Assets.getAssetsPath('qdef'), name + '.qdef')
        if not os.path.isfile(path):
            return
        
        res = ""
        with open(path, 'r', encoding='utf8') as f:
            res = f.read()
            # 按回车分割
            lines = res.split('\n')
            # 清除注释
            lines = [line.split('//')[0] for line in lines]
            # 按分号分隔
            sublines = [subline for subline in [line.split(';') for line in lines]]
            lines = []
            for subline in sublines:
                for sub in subline:
                    sub = sub.strip()
                    if sub != '':
                        lines.append(sub)

            # 读取变量
            for line in lines:
                # 去除空字符
                line = line.strip()
                # 去除分号
                kv = line.split(':')
                if len(kv) == 2:
                    key = kv[0].strip()
                    # 要以$符号开头
                    if key.startswith('$'):
                        value = kv[1].strip()
                        Assets.globalColors[key] = value

                    

    @staticmethod
    def loadQss(name:str, qtinstance=None):
        path = os.path.join(Assets.getAssetsPath('qss'), name + '.qss')
        if not os.path.isfile(path):
            return
    
        res = ""
        with open(path, 'r', encoding='utf8') as f:
            res = f.read()
        if res:
            # 检测变量并替换
            import re
            def convert(value):
                # print(value.groups())
                k = "".join(value.group(1,2))
                v = Assets.globalColors.get(value.group(3))
                r = k+v if v else ""
                if r == "":
                    logger.warning("Couldn't find var key: {}".format(value.group(3)))
                return r
            
            k = re.sub('(?:([^\s;]*)(?:\s*)?)(:(?:[0-9A-Za-z ]*\s*))(\$(?:\s*[^";<>\s]*)*)(?=;|$)', convert, res, 0)
            # print(k)
            if qtinstance:
                qtinstance.setStyleSheet(k)
            else:
                return res

    
    
    @staticmethod
    def loadUi(name:str, qtinstance=None):
        path = os.path.join(Assets.getAssetsPath('ui'), name + '.ui')
        if not os.path.isfile(path):
            return
        
        if qtinstance:
            ui = Assets.uiCache.get(name)
            if not ui:
                logger.debug("loaded uifile succeed: " + path)
                ui = loadUiType(path)[0]
                Assets.uiCache[name] = ui

            qtinstance.ui = ui()
            
            if qtinstance.ui:
                qtinstance.ui.setupUi(qtinstance)
                for k in qtinstance.ui.__dict__:
                    qtinstance.__dict__[k] = qtinstance.ui.__dict__[k]
            else:
                logger.warning("loaded uifile failed: " + path)
        else:
            return qtinstance

