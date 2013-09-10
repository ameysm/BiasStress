from be.imec.biasstress.models.TFT import TFT
from be.imec.biasstress.util.Logger import Logger
from PyQt4 import QtCore
from PyQt4 import QtGui
from be.imec.biasstress.util.Toolbox import isANumber
from be.imec.biasstress.ScriptLoaderDialog import ScriptLoaderDialog
import numpy
from matplotlib.pyplot import legend,gca

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
    
    def __init__(self,devicecontroller,ui,logger,plotcontroller,characteristics,defaultnodevalues):
        AbstractController.__init__(self, devicecontroller)
        self.DEFAULT_VGS_START = defaultnodevalues[0]
        self.DEFAULT_VGS_END= defaultnodevalues[1]
        self.DEFAULT_VDS= defaultnodevalues[3]
        self.DEFAULT_STEP = defaultnodevalues[2]
        self.__ui=ui
        self.__ui.tftwidget.setEnabled(False)
        self.__currentTft = TFT(defaultnodevalues)
        self.__logger=logger
        self.__plotcontroller=plotcontroller
        self.setTFTValues()
        self.__characteristics = characteristics
        self.loadCharacteristics()
    
    def loadCharacteristics(self):
        availableoxides = []
        if len(self.__characteristics)==0:
            raise ValueError('No default TFT characteristics are specified in the settings.xml. Please do so.')
            return
        for k in self.__characteristics:
                availableoxides.append(QtCore.QString(k.getName()))
        self.__ui.oxideCombo.currentIndexChanged['QString'].connect(self.oxideChoiceChanged)
        self.__ui.oxideCombo.addItems(availableoxides)
        
    
    def oxideChoiceChanged(self):
        name = str(self.__ui.oxideCombo.currentText())
        for oxide in self.__characteristics:
            if name == oxide.getName():
                choice = oxide
                break
        if choice == None:
            raise ValueError("Something went wrong what did not supposed to go wrong.")
            return
        
        self.__ui.tft_eps_r.setText(QtCore.QString(choice.getEps_r()))
        self.__ui.tft_t_ox.setText(QtCore.QString(choice.getTox()))
        self.__ui.tft_w.setText(QtCore.QString(choice.getW()))
        self.__ui.tft_l.setText(QtCore.QString(choice.getL()))
        
    
    def resetTFTValues(self):
        self.__ui.vgstart.setText(self.DEFAULT_VGS_START)
        self.__ui.vgend.setText(self.DEFAULT_VGS_END)
        self.__ui.vds.setText(self.DEFAULT_VDS)
        self.__ui.step.setText(self.DEFAULT_STEP)
        self.__logger.log(Logger.INFO,'TFT Values reset')

    
    def setTFTValues(self):
        self.__ui.vgstart.setText(self.__currentTft.getVgStart())
        self.__ui.vgend.setText(self.__currentTft.getVgEnd())
        self.__ui.vds.setText(self.__currentTft.getVds())
        self.__ui.step.setText(self.__currentTft.getStep())
    

    def performSweep(self, gateDevice, drainDevice, gate_smu, drain_smu, start, stop, step):
        self.__logger.log(Logger.INFO, "Performing a TFT sweep from start gate voltage : %s and end gate voltage %e with step size %k", str(start), str(stop), str(step))
        punten = int(abs(stop - start) / step) + 1
        vgs = []
        for i in range(0, punten):
            gate = start + i * step
            vgs.append(gate)
        
        script = 'for x = 1, ' + str(punten) + ' do ' + gate_smu + '.source.levelv = ' + str(start) + ' + x * ' + str(step) + ' delay(0.05) ' + gate_smu + '.measure.i(' + gate_smu + '.nvbuffer1)  ' + drain_smu + '.measure.i(' + drain_smu + '.nvbuffer1) waitcomplete() end count=' + gate_smu + '.nvbuffer1.n print("OK", count)'
        gateDevice.set_output_on()
        gateDevice.write(script)
        readout = gateDevice.read()
        status = readout[0:2]
        if status == 'OK':
            self.__logger.log(Logger.INFO,"The TFT script is done running on the SMU, data will now be extracted and plotted")
        readings = int(float(readout.split('\t')[1]))
        print readings
        igs = gateDevice.readBuffer('nvbuffer1', 1, readings)
        ids = drainDevice.readBuffer('nvbuffer1', 1, readings)
        
        gateDevice.set_output_off()
        return vgs, igs, ids

    def tftRun(self):
        self.__logger.log(Logger.INFO,"Performing a TFT sweep. The GUI will be unresponsive during the run.")
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
        
            
        vgs, igs, ids = self.performSweep(gateDevice, drainDevice, gate_smu, drain_smu, start, stop, step)
        boolFWBW = self.__ui.boolFWBW.isOn()
        if boolFWBW:
            vgs_back,igs_back,ids_back = self.performSweep(gateDevice, drainDevice, gate_smu, drain_smu, stop, start, step)
            self.__plotcontroller.plotIV(ids, igs, vgs,ids_back,igs_back,vgs_back)
            self.__logger.log(Logger.INFO,"Data for forward and backward sweep is plotted")
            return vgs,igs,ids,vgs_back,igs_back,ids_back
        else:
            self.__plotcontroller.plotIV(ids, igs, vgs)
            self.__logger.log(Logger.INFO,"Data for forward sweep is plotted")
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

    def __init__(self,ui,devicecontroller,logger,default_i, default_v):
        self.__ui = ui
        self.__deviceController = devicecontroller
        self.__logger = logger
        self.DEFAULT_I_LIMIT = default_i
        self.DEFAULT_V_LIMIT = default_v
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
        self.__ui.ilim_k1_a.setText(self.DEFAULT_I_LIMIT)
        self.__ui.ilim_k1_b.setText(self.DEFAULT_I_LIMIT)
        self.__ui.ilim_k2_a.setText(self.DEFAULT_I_LIMIT)
        self.__ui.ilim_k2_b.setText(self.DEFAULT_I_LIMIT)
        
        self.__ui.vlim_k1_a.setText(self.DEFAULT_V_LIMIT)
        self.__ui.vlim_k1_b.setText(self.DEFAULT_V_LIMIT)
        self.__ui.vlim_k2_a.setText(self.DEFAULT_V_LIMIT)
        self.__ui.vlim_k2_b.setText(self.DEFAULT_V_LIMIT)
        
    def notifyDeviceAttached(self,device):
        self.__ui.tftwidget.setEnabled(True)
        self.__ui.bias.setEnabled(True)
        print('Device added')
        if self.__k1_address == None and device.getAddress() != self.__k2_address:
            self.__k1_address = device.getAddress()
            self.__ui.ADDRESS_1.setText('Address = '+device.getAddress())
        elif self.__k2_address == None and device.getAddress() != self.__k1_address:
            self.__k2_address = device.getAddress()
            self.__ui.ADDRESS_2.setText('Address = '+device.getAddress())

        self.enableComplianceControls(device.getAddress(), device.getChannel(),device.getNode(),True)
        
    def notifyDeviceRemoved(self,device):
        if len(self.__deviceController.getAllDevices()) == 0:
            self.__ui.tftwidget.setEnabled(False)
            self.__ui.bias.setEnabled(True)
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

'''
Created on Sep 6, 2013

This class controls everything about the scripts.

@author: Incalza Dario
'''

class ScriptController(object):

    def __init__(self,scriptTable,devicecontroller,logger):
        self.__table = scriptTable
        self.__scriptList = []
        self.__devicecontroller = devicecontroller
        self.__logger = logger
    def addScript(self,script):
        if self.__scriptList.count(script) == 0:
            self.__scriptList.append(script)
            self.updateTableView()
        else:
            raise ValueError('This script was already added')
        
    def removeScript(self,script):
        self.__scriptList.remove(script)
        self.updateTableView()
    
    def getScript(self,name):
        for script in self.__scriptList:
            if script.getName() == name:
                return script
        raise ValueError("Script with name %n was not found",name)
    
    def getAllScripts(self):
        return list(self.__scriptList)
    
    def updateTableView(self):
        rows = len(self.__scriptList)
        self.__table.setRowCount(rows)
        x=0
        for script in self.__scriptList:
            self.insertScriptRow(x,script)
            x=x+1
    def getSelectedScript(self):
        selectionModel = self.__table.selectionModel()
        
        if selectionModel.hasSelection():
            rows = selectionModel.selectedRows()
            for idx in rows:
                row = idx.row()
                name = str(self.__table.item(row, 0).text())
                return self.getScript(name)
        else:
            msg = "No script was selected"
            QtGui.QMessageBox.information(None, "Load script..", msg, buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
            
    def loadSelectedScripts(self):
        script = self.getSelectedScript()
        if script == None:
            raise ValueError("Should not happen, script = Nonetype")
        dialog = ScriptLoaderDialog(None,script,self.__devicecontroller,self.__logger)
        dialog.exec_()
        return
            
               
    def insertScriptRow(self,x,script):
        self.__table.setItem(x,0, QtGui.QTableWidgetItem(script.getName()))
        self.__table.setItem(x,1, QtGui.QTableWidgetItem(script.getPath()))
        self.__table.setItem(x,2, QtGui.QTableWidgetItem(script.getSize()+" Kb"))
        
class PlotController(object):

    def __init__(self,plotWidget):
        self.__plotWidget = plotWidget
        
    def PlotFunc(self):
        self.clearPlot()
        self.plotIV([10,100,1000,-100000,100000000],[100,100,100,-100,100],[1,2,3,4,5])
    
    def clearPlot(self):
        self.__plotWidget.canvas.ax.cla()
    
    def plotIV(self,Id,Ig,V,Id_back=None,Ig_back=None,Vg_back = None):
        self.clearPlot()
        Id = numpy.asarray(Id)
        Ig = numpy.asarray(Ig)
        V = numpy.asarray(V)
        self.__plotWidget.canvas.ax.set_title("I-V Curve")
        self.__plotWidget.canvas.ax.set_xlabel("V_gate")
        self.__plotWidget.canvas.ax.set_ylabel("I (log scale)")
        self.__plotWidget.canvas.ax.set_yscale('log')
        self.__plotWidget.canvas.ax.plot(V,numpy.absolute(Id),'g',label='I_ds')
        self.__plotWidget.canvas.ax.plot(V,numpy.absolute(Ig),'r--',label='I_gs')
        if Id_back != None:
            Id_back = numpy.asarray(Id_back)
            Ig_back = numpy.asarray(Ig_back)
            self.__plotWidget.canvas.ax.plot(V,numpy.absolute(Id_back),'b',label='I_ds_back')
            self.__plotWidget.canvas.ax.plot(V,numpy.absolute(Ig_back),'r--',label='I_gs_back')
        legend = self.__plotWidget.canvas.ax.legend(loc='upper center', shadow=True)
        self.__plotWidget.canvas.draw()

        
