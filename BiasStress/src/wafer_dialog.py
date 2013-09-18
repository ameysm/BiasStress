# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wafer_dialog.ui'
#
# Created: Wed Sep 18 09:53:06 2013
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(352, 228)
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 291, 131))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.date_code = QtGui.QLineEdit(self.formLayoutWidget)
        self.date_code.setReadOnly(False)
        self.date_code.setObjectName(_fromUtf8("date_code"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.date_code)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.alias = QtGui.QLineEdit(self.formLayoutWidget)
        self.alias.setObjectName(_fromUtf8("alias"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.alias)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.index_value = QtGui.QSpinBox(self.formLayoutWidget)
        self.index_value.setMinimum(1)
        self.index_value.setObjectName(_fromUtf8("index_value"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.index_value)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.proces_step = QtGui.QLineEdit(self.formLayoutWidget)
        self.proces_step.setObjectName(_fromUtf8("proces_step"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.proces_step)
        self.create_wafer = QtGui.QPushButton(Dialog)
        self.create_wafer.setGeometry(QtCore.QRect(170, 160, 75, 23))
        self.create_wafer.setObjectName(_fromUtf8("create_wafer"))
        self.cancel = QtGui.QPushButton(Dialog)
        self.cancel.setGeometry(QtCore.QRect(250, 160, 75, 23))
        self.cancel.setObjectName(_fromUtf8("cancel"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Wafer Wizard", None))
        self.label.setText(_translate("Dialog", "DATE_CODE    : ", None))
        self.label_2.setText(_translate("Dialog", "ALIAS              :", None))
        self.label_3.setText(_translate("Dialog", "INDEX              :", None))
        self.label_4.setText(_translate("Dialog", "PROCES_STEP :", None))
        self.create_wafer.setText(_translate("Dialog", "Create ...", None))
        self.cancel.setText(_translate("Dialog", "Cancel", None))

