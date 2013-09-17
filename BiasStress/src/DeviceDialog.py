'''
Created on Sep 5, 2013

This class represents a dialog that enables the user to add an SMU device on a particular address and channel.

@author: Incalza Dario
'''
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QDialog
from view_add_device import Ui_addDeviceDialog
from SMU import SMU
from Logger import Logger

class DeviceDialog(QDialog):
   
    def __init__(self,parent,deviceManager,logger):
        self.__deviceManager = deviceManager
        self.__logger = logger
        QtGui.QWidget.__init__(self, parent)
        self.dialog = Ui_addDeviceDialog()
        self.dialog.setupUi(self)
        self.initializeNodeBox()
        self.dialog.pushButton.clicked.connect(self.addDevice)
    def initializeNodeBox(self):
        availableNodes = []
        for k in SMU.NODES:
            if self.__deviceManager.getDeviceMappedToNode(k) == None:
                availableNodes.append(QtCore.QString(k))
        self.dialog.controllingVoltageValue.addItems(availableNodes)
        
    def addDevice(self):
        address = str(self.dialog.adressValue.text())
        channel = str(self.dialog.channelValue.currentText())
        node = str(self.dialog.controllingVoltageValue.currentText())
        smu = self.__deviceManager.tryDeviceConnection(address, channel, node)
        if smu != None:
            succes = self.__deviceManager.addDevice(smu)
            if succes == True:
                self.__logger.log(Logger.INFO,'Device address '+address+' and operating on channel '+channel+' is loaded succesfully and mapped to node : '+smu.getNode()+' \n Additional info :: '+smu.getName())
            else:
                self.__logger.log(Logger.ERROR,'Device on address '+address+' and operating on channel '+channel+' is not loaded succesfully. Please check if the channel or node is not already taken ?')
                
        else:
            self.__logger.log(Logger.ERROR,'Device on address '+address+' and operating on channel '+channel+' is not loaded succesfully. Seems the connection was no initialized correctly. Please ensure the device is turned on and connected through GPIB/USB.')
        self.close() 
        
    