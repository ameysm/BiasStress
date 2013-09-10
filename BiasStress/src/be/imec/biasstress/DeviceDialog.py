'''
Created on Sep 5, 2013

This class represents a dialog that enables the user to add an SMU device on a particular address and channel.

@author: adminssteudel
'''
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QDialog
from views.view_add_device import Ui_addDeviceDialog
from hardware.SMU import SMU
from util.Logger import Logger
import visa
from pyvisa.visa_exceptions import VisaIOError
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
        smu = self.tryDeviceConnection(address, channel, node)
        if smu != None:
            succes = self.__deviceManager.addDevice(smu)
            if succes == True:
                self.__logger.log(Logger.INFO,'Device address '+address+' and operating on channel '+channel+' is loaded succesfully and mapped to node : '+smu.getNode()+' \n Additional info :: '+smu.getName())
            else:
                self.__logger.log(Logger.ERROR,'Device on address '+address+' and operating on channel '+channel+' is not loaded succesfully. Please check if the channel or node is not already taken ?')
                
        else:
            self.__logger.log(Logger.ERROR,'Device on address '+address+' and operating on channel '+channel+' is not loaded succesfully. Seems the connection was no initialized correctly. Please ensure the device is turned on and connected through GPIB/USB.')
        self.close() 
        
    def tryDeviceConnection(self,address,channel,node):
        try:
            device = visa.instrument('GPIB::'+str(address),term_chars='\n', send_end=True)
            name = device.ask("*IDN?")
            smu = SMU(address,channel,node,device,name)
            return smu
        except VisaIOError:
            return None