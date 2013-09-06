'''
Created on Sep 6, 2013

This calss controls everything about the scripts.

@author: Incalza Dario
'''
from PyQt4 import QtGui

class ScriptController(object):

    def __init__(self,scriptTable):
        self.__table = scriptTable
        self.__scriptList = []
        self.__currentTftScript = None
        self.__currentBiasScript = None
    
    def addScript(self,script):
        self.__scriptList.append(script)
        self.updateTableView()
        
    def removeScript(self,script):
        self.__scriptList.remove(script)
        self.updateTableView()
    
    def getAllScripts(self):
        return list(self.__scriptList)
    
    def setTftScript(self,script):
        self.__currentTftScript = script
    
    def setBiasScript(self,script):
        self.__currentBiasScript = script
    
    def getCurrentTftScript(self):
        return self.__currentTftScript
    
    def updateTableView(self):
        rows = len(self.__scriptList)
        self.__table.setRowCount(rows)
        x=0
        for script in self.__scriptList:
            self.insertScriptRow(x,script)
            x=x+1
            
    def insertScriptRow(self,x,script):
        self.__table.setItem(x,0, QtGui.QTableWidgetItem(script.getName()))
        self.__table.setItem(x,1, QtGui.QTableWidgetItem(script.getPath()))
        self.__table.setItem(x,2, QtGui.QTableWidgetItem(script.getSize()))
    
    def getCurrentBiasScript(self):
        return self.__currentBiasScript