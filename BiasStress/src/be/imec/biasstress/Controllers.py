import random
from be.imec.biasstress.models.TFT import TFT
from be.imec.biasstress.util.Logger import Logger
from PyQt4.QtGui import QFileDialog
from PyQt4 import QtCore
import time
from PyQt4 import QtGui
from be.imec.biasstress.util.Toolbox import isANumber
from hardware.SMU import SMU


'''
Created on Sep 5, 2013

This class represents an AbstractController. Which means that this is a base class for other controllers and _SHOULD NOT_ be instantiated. 
Additional Controllers need to extend this class and they will have a VISA controller to handle their hardware communication.

@author: Incalza Dario
'''

class AbstractController(object):
    
    def __init__(self,visa):
        self.__visa=visa
    
    def getDeviceController(self):
        return self.__visa

class TFTController(AbstractController):
    
    def __init__(self,devicecontroller,ui,logger,plotcontroller):
        AbstractController.__init__(self, devicecontroller)
        self.__ui=ui
        self.__currentTft = TFT()
        self.__logger=logger
        self.__plotcontroller=plotcontroller
        self.setTFTValues()
    
    def resetTFTValues(self):
        self.__ui.vgstart.setText(TFT.DEFAULT_VGS_START)
        self.__ui.vgend.setText(TFT.DEFAULT_VGS_END)
        self.__ui.vds.setText(TFT.DEFAULT_VDS)
        self.__ui.step.setText(TFT.DEFAULT_STEP)
        self.__logger.log(Logger.INFO,'TFT Values reset')

    
    def setTFTValues(self):
        self.__ui.vgstart.setText(self.__currentTft.getVgStart())
        self.__ui.vgend.setText(self.__currentTft.getVgEnd())
        self.__ui.vds.setText(self.__currentTft.getVds())
        self.__ui.step.setText(self.__currentTft.getStep())
    
    def tftRun(self):
        gateDevice = self.getDeviceController().getDeviceMappedToNode('Vg')
        drainDevice = self.getDeviceController().getDeviceMappedToNode('Vd')
        gateDevice.clear_buffer()
        drainDevice.clear_buffer()
        if gateDevice == None or drainDevice == None:
            self.__logger.log(Logger.ERROR,"SMU's should be assigned to gate _and_ drain")
        if gateDevice.getAddress() != drainDevice.getAddress():
            self.__logger.log(Logger.ERROR,"Gate and drain should be connected to the same Keithley device.")
            return
    
        if gateDevice.getChannel() == 'A':
            gate_smu = 'smua'
            drain_smu = 'smub'
        else:
            gate_smu = 'smub'
            drain_smu ='smua'
        
        start = int(self.__ui.vgstart.text())
        stop = int(self.__ui.vgend.text())
        step = float(self.__ui.step.text());
        punten = int(abs(stop-start) / step ) + 1
        vgs = []
        for i in range(0,punten):
            gate = start + i * step
            vgs.append(gate)
        
        script = 'for x = 1, ' + str(punten) + ' do '+gate_smu+'.source.levelv = ' + str(start) + ' + x * ' + str(step) + ' delay(0.05) '+gate_smu+'.measure.i('+gate_smu+'.nvbuffer1)  '+drain_smu+'.measure.i('+drain_smu+'.nvbuffer1) waitcomplete() end count='+gate_smu+'.nvbuffer1.n print("OK", count)'        
        gateDevice.set_output_on()
        gateDevice.write(script)
        readout = gateDevice.read()
        status = readout[0:2]
        if status == 'OK':
            print("Script is done")
        
        readings = int(float(readout.split('\t')[1]))
        print readings
        #gateDevice.set_output_off()
        igs = gateDevice.readBuffer('nvbuffer1', 1, readings)
        ids = drainDevice.readBuffer('nvbuffer1', 1, readings)
        self.__plotcontroller.plotIV(ids,vgs);
        return vgs, igs, ids
'''
Created on Sep 5, 2013

@author: Incalza Dario
'''

class DeviceController(AbstractController):
  
    def __init__(self,deviceTableView,visa=None):
        AbstractController.__init__(self, visa)
        self.__deviceList = []
        self.__deviceTable = deviceTableView
        self.__addressList=[]
        self.__nodemapping=dict()
        self.__listeners=[]
        
    def addDevice(self,device):
        if self.getDeviceMappedToNode(device.getNode()) != None:
            return False
        if self.getDevice(device.getDeviceId()) == None :
            self.__deviceList.append(device)
            self.__addressList.append(device.getAddress())
            self.__nodemapping[device.getNode()] = device
            self.updateTableView()
            for listener in self.__listeners:
                listener.notifyDeviceAttached(device)
            return True
        else:
            return False

    def addDeviceListener(self,listener):
        self.__listeners.append(listener)
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
            if device.getAddress() == address:
                if device.getChannel() == 'A':
                    devices.insert(0, device)
                else:
                    devices.insert(1, device)
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
                for listener in self.__listeners:
                    listener.notifyDeviceRemoved(device)
                device.close()
                logger.log(1,'Removed device on address '+device.getAddress()+ ' that was operating on channel '+device.getChannel()+" :: "+device.getName())
        
        self.updateTableView()

class ComplianceController(object):
    DEFAULT_I_LIMIT = '0.1'
    DEFAULT_V_LIMIT = '30'

    def __init__(self,ui,devicecontroller,logger):
        self.__ui = ui
        self.__deviceController = devicecontroller
        self.__logger = logger
        self.disableComplianceControls('all')
        self.__k1_address = None
        self.__k2_address = None
        self.resetDefaults()
        self.registerButtons()
    
    def registerButtons(self):
        self.__ui.apply_compliance_1.clicked.connect(self.applyComplianceK1)
        self.__ui.apply_compliance_2.clicked.connect(self.applyComplianceK2)
    
    def applyComplianceK1(self):
        QtGui.QMessageBox.warning(None, QtCore.QString('Setting compliance levels'), QtCore.QString('This action will set the compliance levels to the given values, be aware this can affect the correct behaviour of the device. Double check the values. '))
        devices = self.__deviceController.getDevicesOnAdress(self.__k1_address)
        if devices != None and len(devices) > 0:
            for device in devices:
                if device.getChannel() == 'A':
                    ilim = str(self.__ui.ilim_k1_a.text())
                    vlim = str(self.__ui.vlim_k1_a.text())
                else:
                    ilim = str(self.__ui.ilim_k1_b.text())
                    vlim = str(self.__ui.vlim_k1_b.text())
            if isANumber(ilim) == False or isANumber(vlim) == False:
                QtGui.QMessageBox.warning(None, QtCore.QString('Error value'), 'Only numerical values are allowed as compliance levels')
                return
            else:
                device.set_current_compliance(str(ilim))
                device.set_voltage_compliance(str(vlim))
                self.__logger.log(Logger.WARNING,"Compliance levels for current and voltage on device "+device.getName()+" are set, respectively, :"+str(ilim)+' A and '+(vlim)+'V'+' for channel '+device.getChannel())
    
    def applyComplianceK2(self):
        QtGui.QMessageBox.warning(None, QtCore.QString('Setting compliance levels'), QtCore.QString('This action will set the compliance levels to the given values, be aware this can affect the correct behaviour of the device. Double check the values. '))
        devices = self.__deviceController.getDevicesOnAdress(self.__k2_address)
        if devices != None and len(devices) > 0:
            for device in devices:
                if device.getChannel() == 'A':
                    ilim = str(self.__ui.ilim_k2_a.text())
                    vlim = str(self.__ui.vlim_k2_a.text())
                else:
                    ilim = str(self.__ui.ilim_k2_b.text())
                    vlim = str(self.__ui.vlim_k2_b.text())
            if isANumber(ilim) == False or isANumber(vlim) == False:
                QtGui.QMessageBox.warning(None, QtCore.QString('Error value'), 'Only numerical values are allowed as compliance levels')
                return
            else:
                device.set_current_compliance(str(ilim))
                device.set_voltage_compliance(str(vlim))
                self.__logger.log(Logger.WARNING,"Compliance levels for current and voltage on device "+device.getName()+" are set, respectively, :"+str(ilim)+' A and '+(vlim)+'V'+' for channel '+device.getChannel())              
    
    def resetDefaults(self):
        self.__ui.ilim_k1_a.setText(ComplianceController.DEFAULT_I_LIMIT)
        self.__ui.ilim_k1_b.setText(ComplianceController.DEFAULT_I_LIMIT)
        self.__ui.ilim_k2_a.setText(ComplianceController.DEFAULT_I_LIMIT)
        self.__ui.ilim_k2_b.setText(ComplianceController.DEFAULT_I_LIMIT)
        
        self.__ui.vlim_k1_a.setText(ComplianceController.DEFAULT_V_LIMIT)
        self.__ui.vlim_k1_b.setText(ComplianceController.DEFAULT_V_LIMIT)
        self.__ui.vlim_k2_a.setText(ComplianceController.DEFAULT_V_LIMIT)
        self.__ui.vlim_k2_b.setText(ComplianceController.DEFAULT_V_LIMIT)
        
    def notifyDeviceAttached(self,device):
        print('Device added')
        if self.__k1_address == None and device.getAddress() != self.__k2_address:
            self.__k1_address = device.getAddress()
            self.__ui.ADDRESS_1.setText('Address = '+device.getAddress())
        elif self.__k2_address == None and device.getAddress() != self.__k1_address:
            self.__k2_address = device.getAddress()
            self.__ui.ADDRESS_2.setText('Address = '+device.getAddress())

        self.enableComplianceControls(device.getAddress(), device.getChannel(),device.getNode(),True)
        
    def notifyDeviceRemoved(self,device):
        print('Device removed')
        self.enableComplianceControls(device.getAddress(), device.getChannel(),device.getNode(),False)
        
    def disableComplianceControls(self,command):
        if command == 'all':
            self.__ui.box_k1_a.setEnabled(False)
            self.__ui.box_k1_b.setEnabled(False)
            self.__ui.box_k2_a.setEnabled(False)
            self.__ui.box_k2_b.setEnabled(False)
            
        if command == 'k1':
            self.__ui.box_k1_a.setEnabled(False)
            self.__ui.box_k1_b.setEnabled(False)
            
        if command == 'k2':
            self.__ui.box_k2_a.setEnabled(False)
            self.__ui.box_k2_b.setEnabled(False)
    
    def enableComplianceControls(self,address,channel,node,boolToggle):
        if self.__k1_address == address:
            if channel == 'A':
                self.__ui.node_k1_a.setText(node)
                self.__ui.box_k1_a.setEnabled(boolToggle)
            else:
                self.__ui.node_k1_b.setText(node)
                self.__ui.box_k1_b.setEnabled(boolToggle)
        else:
            if channel == 'A':
                self.__ui.node_k2_a.setText(node)
                self.__ui.box_k2_a.setEnabled(boolToggle)
            else:
                self.__ui.node_k2_b.setText(node)
                self.__ui.box_k2_b.setEnabled(boolToggle)

    
class PlotController(object):

    def __init__(self,plotWidget):
        self.__plotWidget = plotWidget
        
    def PlotFunc(self):
        self.clearPlot()
        randomNumbers = random.sample(range(0, 10), 10)
        self.__plotWidget.canvas.ax.set_title("I-V Curve")
        self.__plotWidget.canvas.ax.set_xlabel("V")
        self.__plotWidget.canvas.ax.set_ylabel("I")
        self.__plotWidget.canvas.ax.plot(randomNumbers)
        self.__plotWidget.canvas.draw()
    
    def clearPlot(self):
        self.__plotWidget.canvas.ax.cla()
    
    def plotIV(self,I,V):
        self.clearPlot()
        self.__plotWidget.canvas.ax.set_title("I-V Curve")
        self.__plotWidget.canvas.ax.set_xlabel("V")
        self.__plotWidget.canvas.ax.set_ylabel("I")
        self.__plotWidget.canvas.ax.plot(V,I)
        self.__plotWidget.canvas.draw()

        
