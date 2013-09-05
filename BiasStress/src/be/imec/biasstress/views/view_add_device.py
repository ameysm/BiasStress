# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view_add_device.ui'
#
# Created: Thu Sep 05 16:44:26 2013
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

class Ui_addDeviceDialog(object):
    def setupUi(self, addDeviceDialog):
        addDeviceDialog.setObjectName(_fromUtf8("addDeviceDialog"))
        addDeviceDialog.resize(230, 165)
        self.pushButton = QtGui.QPushButton(addDeviceDialog)
        self.pushButton.setGeometry(QtCore.QRect(120, 120, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.formLayoutWidget = QtGui.QWidget(addDeviceDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 166, 91))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.adressValue = QtGui.QSpinBox(self.formLayoutWidget)
        self.adressValue.setMaximum(30)
        self.adressValue.setProperty("value", 27)
        self.adressValue.setObjectName(_fromUtf8("adressValue"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.adressValue)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.channelValue = QtGui.QComboBox(self.formLayoutWidget)
        self.channelValue.setObjectName(_fromUtf8("channelValue"))
        self.channelValue.addItem(_fromUtf8(""))
        self.channelValue.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.channelValue)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.controllingVoltageValue = QtGui.QComboBox(self.formLayoutWidget)
        self.controllingVoltageValue.setObjectName(_fromUtf8("controllingVoltageValue"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.controllingVoltageValue)

        self.retranslateUi(addDeviceDialog)
        QtCore.QMetaObject.connectSlotsByName(addDeviceDialog)

    def retranslateUi(self, addDeviceDialog):
        addDeviceDialog.setWindowTitle(_translate("addDeviceDialog", "Dialog", None))
        self.pushButton.setText(_translate("addDeviceDialog", "Add device..", None))
        self.label.setText(_translate("addDeviceDialog", "Address             ", None))
        self.label_2.setText(_translate("addDeviceDialog", "Channel", None))
        self.channelValue.setItemText(0, _translate("addDeviceDialog", "A", None))
        self.channelValue.setItemText(1, _translate("addDeviceDialog", "B", None))
        self.label_3.setText(_translate("addDeviceDialog", "Node", None))

