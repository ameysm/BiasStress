'''
Created on Sep 5, 2013

@author: Incalza Dario
'''
from AbstractController import AbstractController
from PyQt4 import QtGui
class DeviceController(AbstractController):
  
    def __init__(self,deviceTableView,visa=None):
        AbstractController.__init__(self, visa)
        self.__deviceList = []
        self.__deviceTable = deviceTableView
        
    def addDevice(self,device):
        if self.getDevice(device.getDeviceId()) == None :
            self.__deviceList.append(device)
            self.updateTableView(device)
            return True
        else:
            return False
        
    def getDevice(self,deviceid):
        for device in self.__deviceList:
            if device.getDeviceId() == deviceid:
                return device
        return None
    
    def getAllDevices(self):
        return self.__deviceList
    
    def updateTableView(self,device):
        rows = len(self.__deviceList)
        self.__deviceTable.setRowCount(rows)
        for device in self.__deviceList:
            for x in range(0,rows+1):
                self.__deviceTable.setItem(x,0, QtGui.QTableWidgetItem(device.getName()))
                self.__deviceTable.setItem(x,1, QtGui.QTableWidgetItem(device.getChannel()))
                self.__deviceTable.setItem(x,2, QtGui.QTableWidgetItem(device.getAddress()))
                self.__deviceTable.setItem(x,3, QtGui.QTableWidgetItem(device.getNode()))
