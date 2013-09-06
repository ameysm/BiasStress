'''
Created on Sep 6, 2013

@author: adminssteudel
'''
import random 

class PlotController(object):
    '''
    classdocs
    '''


    def __init__(self,plotWidget):
        self.__plotWidget = plotWidget
        
    def PlotFunc(self):
        self.clearPlot()
        randomNumbers = random.sample(range(0, 10), 10)
        self.__plotWidget.canvas.ax.set_title("I-V Curve")
        self.__plotWidget.canvas.ax.set_xlabel("V")
        self.__plotWidget.canvas.ax.set_ylabel("I")
        self.__plotWidget.canvas.ax.plot(randomNumbers)
        self.__plotWidget.canvas.draw()
    
    def clearPlot(self):
        self.__plotWidget.canvas.ax.cla()
    
        