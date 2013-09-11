'''
Created on Sep 9, 2013

This dialog will be shown when the user wants to upload a script to a particular device

@author: Incalza Dario
'''
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui
from be.imec.biasstress.views.script_loader import Ui_ScriptLoader
from util.Logger import Logger
class ScriptLoaderDialog(QDialog):
    

    def __init__(self,parent,script,devicecontroller,logger):
        self.__script = script
        self.__devicecontroller = devicecontroller
        self.__logger = logger
        QtGui.QWidget.__init__(self, parent)
        self.dialog = Ui_ScriptLoader()
        self.dialog.setupUi(self)
        self.initializeScriptBox()
        self.dialog.okButton.clicked.connect(self.okClicked)
        self.dialog.cancelButton.clicked.connect(self.close)
    def initializeScriptBox(self):
        addresses = self.__devicecontroller.getActiveAdresses()
        if len(addresses) == 0:
            self.dialog.okButton.setEnabled(False)
            return
        x=0
        for address in addresses:
            self.dialog.tableWidget.setItem(x,0,QtGui.QTableWidgetItem(address))
            device = self.__devicecontroller.getDevicesOnAdress(address)[0]
            self.dialog.tableWidget.setItem(x,1,QtGui.QTableWidgetItem(device.getName()))
    
    def okClicked(self):
        selectionModel = self.dialog.tableWidget.selectionModel()
        
        if selectionModel.hasSelection():
            rows = selectionModel.selectedRows()
            for idx in rows:
                row = idx.row()
                address = str(self.dialog.tableWidgetitem(row, 0).text())
                device = self.__devicecontroller.getDevicesOnAdress(address)
                device.loadScript(self.__script)
                self.__logger.log(Logger.INFO,"The script %n was loaded on address %a",self.__script.getName(),address)
                self.close()
                return
                
        else:
            msg = "No device was selected"
            QtGui.QMessageBox.information(None, "Load script on device..", msg, buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)