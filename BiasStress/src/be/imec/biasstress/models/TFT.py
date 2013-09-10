'''
Created on Sep 4, 2013

This class represents an TFT run. Default values are given.

@author: Incalza Dario
'''

class TFT(object):    
    
    def __init__(self,defaultvalues):
        self.__vgStart = defaultvalues[0]
        self.__vgEnd =defaultvalues[1]
        self.__vds = defaultvalues[3]
        self.__step = defaultvalues[2]
    
    def getVgStart(self):
        return self.__vgStart
    
    def getVgEnd(self):
        return self.__vgEnd
    
    def getVds(self):
        return self.__vds
    
    def getStep(self):
        return self.__step
    
    def setStep(self,step):
        self.__step = step
        
    def setVgStart(self,vgsstart):
        self.__vgStart = vgsstart
    
    def setVds(self,vds):
        self.__vds
        
    def setVgEnd(self, vgend):
        self.__vgEnd = vgend