'''
Created on Sep 4, 2013

This represents the main program window connecting the GUI to the backend logic, initializing controllers and passing control.

@author: Incalza Dario
'''
from PyQt4 import QtGui,QtCore
from views.main_view import Ui_MainWindow
from util.Logger import Logger
from DeviceDialog import DeviceDialog
import os
from models.Script import Script
from Controllers import TFTController,DeviceController,ComplianceController,PlotController,ScriptController,DatabaseController,BiasController
from Settings import SettingsParser
import sys
class BiasStress(QtGui.QMainWindow):
   
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_MainWindow()    #note: instance, not the class
        self.ui.setupUi(self)
        self.__logger = Logger(self.ui.logConsole)
        
        try:
            self.__settingsParser = SettingsParser()
            self.__settingsParser.parse()
            self.__deviceController = DeviceController(self.ui)
            self.__complianceController = ComplianceController(self.ui,self.__deviceController,self.__logger,self.__settingsParser.getConstantValue('compliance_current'),self.__settingsParser.getConstantValue('compliance_voltage'));
            self.__deviceController.addDeviceListener(self.__complianceController)
            self.__scriptController = ScriptController(self.ui.scriptTable,self.__deviceController,self.__logger)
            self.__plotController = PlotController(self.ui.plotWidget)
            self.__tftController = TFTController(self.__deviceController,self.ui,self.__logger,self.__plotController,self.__settingsParser.getTFTCharacteristics(),self.__settingsParser.getDefaultTFTNodeValues())
            self.__dbController = DatabaseController(self.ui,self.__logger,self.__tftController)
            self.__biasController = BiasController(self.ui,self.__logger,self.__tftController,self.__deviceController,self.__plotController)
            self.initialize_gui()
        except IOError:
            QtGui.QMessageBox.warning(None, QtCore.QString('Error settings'), 'The settings file is either missing or has the wrong syntax. Please ensure there is a file "settings.xml" present in the root directory of this application. Aborting.')
            sys.exit()
     
    def initialize_gui(self):
        self.register_gui_functions()
        #self.ui.bias.setEnabled(False)
        self.ui.tftwidget.setEnabled(False)
        self.initializeBiasDefault()
        self.__logger.log(Logger.INFO,"###### Welcome to BiasStress ######")
    
    def initializeBiasDefault(self):
        self.ui.stressGateVoltage.setText(self.__settingsParser.getBiasConfig("stress-gate-voltage"))
        self.ui.drainStressVoltage.setText(self.__settingsParser.getBiasConfig("stress-drain-voltage"))
        self.ui.samplesPerDecade.setValue(int(self.__settingsParser.getBiasConfig("default-decades")))
        self.ui.totalTime.setText(self.__settingsParser.getBiasConfig("default-total-stress-time"))
        self.ui.positiveBiasDirection.setChecked(True)
        
    def register_gui_functions(self):
        self.ui.actionQuit.triggered.connect(QtGui.qApp.quit)
        self.ui.resetTFT.clicked.connect(self.__tftController.resetTFTValues)
        self.ui.clearLogAction.clicked.connect(self.__logger.clearLog)
        self.ui.saveLogAction.clicked.connect(self.__logger.saveLog)
        self.ui.actionAddDevice.clicked.connect(self.showAddDeviceDialog)
        self.ui.boolAdvancedScripting.clicked.connect(self.toggleAdvanceScripting)
        self.ui.actionRemoveDevice.clicked.connect(self.deleteDevice)
        self.ui.openScript.clicked.connect(self.openScript)
        self.ui.runTFT.clicked.connect(self.__tftController.tftRun)
        self.ui.loadScriptToDevice.clicked.connect(self.__scriptController.loadSelectedScripts)
        self.ui.actionAutoConnect.clicked.connect(self.autoConnectDevices)
        self.ui.actionBiasResetDefault.clicked.connect(self.initializeBiasDefault)
        
        ##db actions
        self.ui.actionOpenDatabase.clicked.connect(self.__dbController.chooseDatabaseFile)
        self.ui.actionNewDb.clicked.connect(self.__dbController.createNewDbFile)
        self.ui.actionSaveTFTConfig.clicked.connect(self.__dbController.saveTftConfiguration)
    
    def showAddDeviceDialog(self):
       
        dialog = DeviceDialog(self,self.__deviceController,self.__logger)
        dialog.exec_()
        
    def toggleAdvanceScripting(self):
        if self.ui.boolAdvancedScripting.checkState() == QtCore.Qt.Checked:
            accept_msg = "Are you sure you want to enter advanced scripting mode ?"
            reply = QtGui.QMessageBox.question(self, 'Advanced Scripting Mode', 
                             accept_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    
            if reply == QtGui.QMessageBox.Yes:
                boolScripting = True
                self.__logger.log(Logger.WARNING, "User entered advanced scripting mode. The scripts edited through this interface will be uploaded unconditionally and syntax is not verified.")
            else:
                self.ui.boolAdvancedScripting.toggle()
                return
        else:
            boolScripting = False
            self.__logger.log(Logger.INFO, "User exited advanced scripting mode.")
        self.ui.scriptEditor.setEnabled(boolScripting)
        self.ui.openAdvancedScript.setEnabled(boolScripting)
        self.ui.uploadAdvancedScript.setEnabled(boolScripting)
    
    def deleteDevice(self):
        selectionModel = self.ui.deviceTable.selectionModel()
        deviceIds=[]
        if selectionModel.hasSelection():
            rows = selectionModel.selectedRows()
            
            for idx in rows:
                row = idx.row()
                item_address = self.ui.deviceTable.item(row, 2)
                item_channel = self.ui.deviceTable.item(row, 1)
                device_id = item_channel.text()+item_address.text()
                deviceIds.append(device_id)
                
            for idz in deviceIds:
                self.__deviceController.deleteDevicesById(idz,self.__logger)
        else:
            msg = "No devices where selected"
            QtGui.QMessageBox.information(self, "Remove devices", msg, buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
    
    def autoConnectDevices(self):
        for (node,address,channel) in self.__settingsParser.getDefaultDevices():
            smu = self.__deviceController.tryDeviceConnection(address, channel, node)
            if smu != None:
                succes = self.__deviceController.addDevice(smu)
                if succes == True:
                    self.__logger.log(Logger.INFO,'Default device address '+address+' and operating on channel '+channel+' is loaded succesfully and mapped to node : '+smu.getNode()+' \n Additional info :: '+smu.getName())
                else:
                    self.__logger.log(Logger.WARNING,'Default device on address '+address+' and operating on channel '+channel+' is not loaded succesfully. Please check if the channel or node is not already taken ?')
                    
            else:
                self.__logger.log(Logger.WARNING,'Default device on address '+address+' and operating on channel '+channel+' is not loaded succesfully. Seems the connection was no initialized correctly. Please ensure the device is turned on and connected through GPIB/USB.')
    
    def openScript(self):
        path = str(QtGui.QFileDialog.getOpenFileName(self, 'Load Script...', '/home','*.txt'))
        if path.strip() =="":
            return
        fname = os.path.basename(str(path))
        size = os.path.getsize(path)*0.001
        script = Script(fname,path,size)
        try:
            self.__scriptController.addScript(script)
            self.__logger.log(Logger.INFO, "Script opened : "+fname+" size = "+str(size)+" Kb")
        except ValueError:
            self.__logger.log(Logger.WARNING,"This script was already opened in the application.")