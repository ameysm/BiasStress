'''
Created on Sep 13, 2013

This dialog enbles the user to create a new wafer and start measurements for it.

@author: Incqlza Dario
'''
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui,QtCore
from wafer_dialog import Ui_Dialog 
from datetime import datetime
import os,errno
from Wafer import Wafer
class WaferDialog(QDialog):
    

    def __init__(self,parent,wafercontroller,logger,working_dir):
        self.__wafercontroller = wafercontroller
        self.__logger = logger
        self.__working_dir = working_dir
        QtGui.QWidget.__init__(self, parent)
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.dialog.date_code.setText(str(datetime.now().strftime("%Y%m%d")))
        self.dialog.create_wafer.clicked.connect(self.okClicked)
        self.dialog.cancel.clicked.connect(self.close)

    def okClicked(self):
        alias = str(self.dialog.alias.text())
        proc_step = str(self.dialog.proces_step.text())
        index = str(self.dialog.index_value.text())
        date_code = str(self.dialog.date_code.text())
        if alias.strip() =="" or proc_step.strip() == "" or index.strip() == "" or date_code.strip=="":
            QtGui.QMessageBox.warning(None, QtCore.QString('Value error'), QtCore.QString('One or more invalid values were detected. Make sure non are empty.'))
            return
        try:
            self.createWaferDir(alias,date_code,index)
        except OSError:
            QtGui.QMessageBox.warning(None, QtCore.QString('Direction error'), QtCore.QString('Do you have read and write rights in the working directory, specified in settings.xml ?'))
            return
        wafer = Wafer(date_code, index, proc_step, alias)
        self.__wafercontroller.addWafer(wafer)
        self.__wafercontroller.setCurrentWafer(wafer)
        self.close()
    
    def createWaferDir(self,alias,date_code,index):
        path = self.__working_dir+"//"+alias+date_code+"//"+index
        if os.path.isdir(path) == True :
            return
        else:
            try:
                os.makedirs(path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise