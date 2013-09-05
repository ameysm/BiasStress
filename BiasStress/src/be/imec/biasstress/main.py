'''
Created on Sep 4, 2013

@author: Incalza Dario
'''
from PyQt4 import QtGui
import sys
from BiasStress import BiasStress

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.processEvents()
    controller = BiasStress()
    controller.show()
    sys.exit(app.exec_())

