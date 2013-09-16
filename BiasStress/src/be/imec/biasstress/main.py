'''
Created on Sep 4, 2013

This is the main entry point of the program.

@author: Incalza Dario
'''
from PyQt4 import QtGui
import sys,time
from BiasStress import BiasStress

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    splash_pix = QtGui.QPixmap('splash.png')
    splash = QtGui.QSplashScreen(splash_pix)
    splash.show()
    app.processEvents()
    controller = BiasStress()
    time.sleep(3)
    splash.finish(controller)
    controller.show()
    sys.exit(app.exec_())

