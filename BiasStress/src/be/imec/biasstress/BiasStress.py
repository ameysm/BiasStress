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
from Controllers import TFTController,DeviceController,ComplianceController,PlotController,ScriptController
from Settings import SettingsParser
import sys
class BiasStress(QtGui.QMainWindow):
    '''
    classdocs
    '''
    def __init__(self,parent=None):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_MainWindow()    #note: instance, not the class
        self.ui.setupUi(self)
        self.__logger = Logger(self.ui.logConsole)
        '''
        try:
            self.__settingsParser = SettingsParser()
            self.__settingsParser.parse()
            self.__deviceController = DeviceController(self.ui.deviceTable)
            self.__complianceController = ComplianceController(self.ui,self.__deviceController,self.__logger);
            self.__deviceController.addDeviceListener(self.__complianceController)
            self.__scriptController = ScriptController(self.ui.scriptTable,self.__deviceController,self.__logger)
            self.__plotController = PlotController(self.ui.plotWidget)
            self.__tftController = TFTController(self.__deviceController,self.ui,self.__logger,self.__plotController)
            self.initialize_gui()
        except IOError:
            QtGui.QMessageBox.warning(None, QtCore.QString('Error settings'), 'The settings file is either missing or has the wrong syntax. Aborting.')
            sys.exit()
        '''
        self.__deviceController = DeviceController(self.ui.deviceTable)
        self.__complianceController = ComplianceController(self.ui,self.__deviceController,self.__logger);
        self.__deviceController.addDeviceListener(self.__complianceController)
        self.__scriptController = ScriptController(self.ui.scriptTable,self.__deviceController,self.__logger)
        self.__plotController = PlotController(self.ui.plotWidget)
        self.__tftController = TFTController(self.__deviceController,self.ui,self.__logger,self.__plotController)
        self.initialize_gui()
        
    
    def initialize_gui(self):
        self.register_gui_functions()
        self.ui.bias.setEnabled(False)
        self.__logger.log(Logger.INFO,"###### Welcome to BiasStress ######")
        
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

    def openScript(self):
        path = QtGui.QFileDialog.getOpenFileName(self, 'Load Script...', '/home','*.txt')
        fname = os.path.basename(str(path))
        size = os.path.getsize(path)*0.001
        script = Script(fname,path,size)
        try:
            self.__scriptController.addScript(script)
            self.__logger.log(Logger.INFO, "Script opened : "+fname+" size = "+str(size)+" Kb")
        except ValueError:
            self.__logger.log(Logger.WARNING,"This script was already opened in the application.")