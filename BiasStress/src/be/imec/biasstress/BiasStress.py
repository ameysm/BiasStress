'''
Created on Sep 4, 2013

@author: Incalza Dario
'''
from PyQt4 import QtGui
from views.main_view import Ui_MainWindow
from util.Logger import Logger
from be.imec.biasstress.controllers.TFTController import TFTController
from DeviceDialog import DeviceDialog
from controllers.DeviceController import DeviceController

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
        self.initialize_gui()
        self.__deviceController = DeviceController(self.ui.deviceTable)
    
    def initialize_gui(self):
        self.__logger = Logger(self.ui.logConsole)
        self.register_gui_functions()
        self.__logger.log(Logger.INFO,"###### Welcome to BiasStress ######")
        
    def register_gui_functions(self):
        self.ui.actionQuit.triggered.connect(QtGui.qApp.quit)
        self.__tftController = TFTController(self,self.ui,self.__logger)
        self.ui.resetTFT.clicked.connect(self.__tftController.resetTFTValues)
        self.ui.clearLogAction.clicked.connect(self.__logger.clearLog)
        self.ui.saveLogAction.clicked.connect(self.__logger.saveLog)
        self.ui.actionAddDevice.clicked.connect(self.showAddDeviceDialog)
    
    def showAddDeviceDialog(self):
        dialog = DeviceDialog(self,self.__deviceController,self.__logger)
        dialog.exec_()
        

    