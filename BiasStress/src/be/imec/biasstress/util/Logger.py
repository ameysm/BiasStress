'''
Created on Sep 4, 2013

@author: Incalza Dario
'''
from datetime import datetime
from PyQt4.QtGui import QColor
from PyQt4 import QtGui,QtCore

class Logger(object):
   
    INFO=0x0
    WARNING=0x1
    ERROR=0x2
    '''
    A given console that is a text widget in the gui.
    '''
    def __init__(self,console):
        self.__console = console
        self.__console.setTextBackgroundColor(QColor(0,0,0))
    '''
    Log a text to inform the user of a certain IO action. Given : the text that needs to be displayed. A timestamp will be printed before the text.
    '''
    def log(self,level,text):
        if level==0x0:
            color = QColor(124, 252, 0)
            prefix=' - [Info]'
        elif level == 0x1:
            color = QColor(255,140,0)
            prefix=' - [Warning]'
        else:
            color = QColor(253,0,0)
            prefix=' - [Error]'
        self.__console.setTextColor(color)
        now = datetime.now()
        time = str(now.strftime("%H:%M"))
        self.__console.append(time+prefix+" >> "+text)
    
    def clearLog(self):
        self.__console.clear()
    
    def saveLog(self):
        filename = "biasstress_log_"+str(datetime.now().strftime("%d%m%y-%H%M"))
        path = QtGui.QFileDialog.getSaveFileName(None, QtCore.QString('Open file'), QtCore.QString(filename),".txt")
        text_file = open(path, "w")
        text_file.write(self.__console.toPlainText())
        text_file.close()