# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'script_loader.ui'
#
# Created: Tue Sep 10 09:12:07 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ScriptLoader(object):
    def setupUi(self, ScriptLoader):
        ScriptLoader.setObjectName(_fromUtf8("ScriptLoader"))
        ScriptLoader.resize(380, 281)
        self.verticalLayoutWidget = QtGui.QWidget(ScriptLoader)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 361, 242))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.tableWidget = QtGui.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ScriptLoader)
        QtCore.QMetaObject.connectSlotsByName(ScriptLoader)

    def retranslateUi(self, ScriptLoader):
        ScriptLoader.setWindowTitle(_translate("ScriptLoader", "ScriptLoader", None))
        self.label.setText(_translate("ScriptLoader", "Choose the device to which the script should be uploaded.", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ScriptLoader", "ADDRESS", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ScriptLoader", "NAME", None))
        self.okButton.setText(_translate("ScriptLoader", "Load script on selected device", None))
        self.cancelButton.setText(_translate("ScriptLoader", "Cancel", None))

