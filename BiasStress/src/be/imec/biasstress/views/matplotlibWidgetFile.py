'''
Created on Sep 6, 2013

@author: Incalza Dario
'''

from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
 
class MplCanvas(FigureCanvas):
 
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
 
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
 
 
class matplotlibWidget(QtGui.QWidget):
 
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.canvas.ax.set_title("I-V Curve")
        self.canvas.ax.set_xlabel("V")
        self.canvas.ax.set_ylabel("I")
        self.toolbar = NavigationToolbar2QT(self.canvas, None, True)
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)

