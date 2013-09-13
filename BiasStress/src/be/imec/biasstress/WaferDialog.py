'''
Created on Sep 13, 2013

@author: adminssteudel
'''
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui,QtCore
from be.imec.biasstress.views.wafer_dialog import Ui_Dialog 
from datetime import datetime
from be.imec.biasstress.models.Wafer import Wafer
class WaferDialog(QDialog):
    

    def __init__(self,parent,wafercontroller,logger):
        self.__wafercontroller = wafercontroller
        self.__logger = logger
        QtGui.QWidget.__init__(self, parent)
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.dialog.date_code.setText(str(datetime.now().strftime("%y%m%d")))
        self.dialog.create_wafer.clicked.connect(self.okClicked)
        self.dialog.cancel.clicked.connect(self.close)

    def okClicked(self):
        alias = str(self.dialog.alias.text())
        proc_step = str(self.dialog.proces_step.text())
        index = str(self.dialog.index_value.text())
        date_code = str(self.dialog.date_code.text())
        if alias.strip() =="" or proc_step.strip() == "" or index.strip() == "" or date_code.strip=="":
            QtGui.QMessageBox.warning(None, QtCore.QString('Value error'), QtCore.QString('One or more invalid values were detected.'))
            return
        
        wafer = Wafer(date_code, index, proc_step, alias)
        self.__wafercontroller.addWafer(wafer)
        self.__wafercontroller.setCurrentWafer(wafer)
        self.close()