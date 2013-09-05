'''
Created on Sep 5, 2013

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
        self.NODES = dict(Vg=0x00, Vd=0x01, Vs=0x02)
        self.NODES_ENTRIES=[]
        for k in self.NODES:
            self.NODES_ENTRIES.append(QtCore.QString(k))
        QtGui.QWidget.__init__(self, parent)
        self.dialog = Ui_addDeviceDialog()
        self.dialog.setupUi(self)
        self.dialog.controllingVoltageValue.addItems(self.NODES_ENTRIES)
        self.dialog.pushButton.clicked.connect(self.addDevice)
    
    def addDevice(self):
        address = str(self.dialog.adressValue.text())
        channel = str(self.dialog.channelValue.currentText())
        node = str(self.dialog.controllingVoltageValue.currentText())
        smu = self.tryDeviceConnection(address, channel, node)
        if smu != None:
            succes = self.__deviceManager.addDevice(smu)
            if succes == True:
                self.__logger.log(Logger.INFO,'Device on address '+address+' and operating on channel '+channel+' is loaded succesfully')
        else:
            self.__logger.log(Logger.ERROR,'Device on address '+address+' and operating on channel '+channel+' is not loaded succesfully. Please check GPIB/USB connection and ensure the device is powered on before trying again.')
        self.close() 
        
    def tryDeviceConnection(self,address,channel,node):
        try:
            device = visa.instrument('GPIB::'+str(address))
            name = device.ask("*IDN?")
            smu = SMU(address,channel,node,device,name)
            return smu
        except VisaIOError:
            return None