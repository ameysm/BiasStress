'''
Created on Sep 4, 2013

This class represents an TFT run. Default values are given.

@author: Incalza Dario
'''

class TFT(object):
    '''
    Default vars for a TFT
    __WARNING__ These values are used thoughout the program, make sure these are the correct default values
    '''
    DEFAULT_VGS_START = '-20'
    DEFAULT_VGS_END= '20'
    DEFAULT_VDS='1'
    DEFAULT_STEP='2e-1'
    
    
    def __init__(self,defaultvalues):
        
        
        self.__vgStart = TFT.DEFAULT_VGS_START
        self.__vgEnd =TFT.DEFAULT_VGS_END
        self.__vds = TFT.DEFAULT_VDS
        self.__step = TFT.DEFAULT_STEP
    
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