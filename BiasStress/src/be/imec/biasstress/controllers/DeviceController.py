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
        self.__addressList=[]
        self.__nodemapping=dict()
        
    def addDevice(self,device):
        if self.getDeviceMappedToNode(device.getNode()) != None:
            return False
        if self.getDevice(device.getDeviceId()) == None :
            self.__deviceList.append(device)
            self.__addressList.append(device.getAddress())
            self.__nodemapping[device.getNode()] = device
            self.updateTableView()
            return True
        else:
            return False
        
    def getDeviceMappedToNode(self,node):
        return self.__nodemapping.get(node)

    def removeMappingNode(self,node):
        self.__nodemapping.pop(node)
        
    def getDevice(self,deviceid):
        for device in self.__deviceList:
            if device.getDeviceId() == deviceid:
                return device
        return None
    
    def getActiveAdresses(self):
        return self.__addressList
    
    def getDevicesOnAdress(self,address):
        devices=[]
        for device in self.__deviceList:
            if device.getAdress() == address:
                if device.getChannel() == 'A':
                    devices.insert(0, device)
                else:
                    devices.insert(1, device)
                devices.append(device)
        return devices
                
    def getAllDevices(self):
        return self.__deviceList
    
    def updateTableView(self):
        rows = len(self.__deviceList)
        self.__deviceTable.setRowCount(rows)
        x=0
        for device in self.__deviceList:
            self.insertDeviceRow(x,device)
            x=x+1
            
    def insertDeviceRow(self,x,device):
        self.__deviceTable.setItem(x,0, QtGui.QTableWidgetItem(device.getName()))
        self.__deviceTable.setItem(x,1, QtGui.QTableWidgetItem(device.getChannel()))
        self.__deviceTable.setItem(x,2, QtGui.QTableWidgetItem(device.getAddress()))
        self.__deviceTable.setItem(x,3, QtGui.QTableWidgetItem(device.getNode()))
    
    def deleteDevicesById(self,idx,logger):        
        for device in list(self.__deviceList.__iter__()):
            if device.getDeviceId() == idx:
                self.__deviceList.remove(device)
                self.removeMappingNode(device.getNode())
                logger.log(1,'Removed device on address '+device.getAddress()+ ' that was operating on channel '+device.getChannel()+" :: "+device.getName())
        
        self.updateTableView()
        
