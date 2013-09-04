'''
Created on Sep 4, 2013

@author: Incalza Dario
'''
from PyQt4 import QtGui
from views.main_view import Ui_MainWindow
from util.Logger import Logger

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
    
    def initialize_gui(self):
        self.__logger = Logger(self.ui.logConsole)
        self.register_gui_functions()
        self.__logger.log("###### Welcome to BiasStress ######")
        self.checkforDevices()
        
    def register_gui_functions(self):
        self.ui.actionQuit.triggered.connect(QtGui.qApp.quit)
        pass
    
    def checkforDevices(self):
        self.__listDevices = []
        self.__logger.log("0 devices were found")