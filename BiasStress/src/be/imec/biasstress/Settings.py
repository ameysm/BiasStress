'''
Created on Sep 10, 2013

@author: Incalza Dario
'''
from xml.dom import minidom
'''
This class is responsible for parsing the settings.xml file. 
'''
class SettingsParser(object):
    
    def __init__(self):
        self.__xmldoc = minidom.parse('../../../../settings.xml')
    
    def parse(self):
        self.parseTftCharacteristics()
        self.parseConstants()
        
    def parseTftCharacteristics(self):
        characteristiclist = self.__xmldoc.getElementsByTagName('characteristic')
        self.__characteristics = [] 
        for c in characteristiclist :
            characteristic = TFTCharacteristic(c.attributes['name'].value,c.attributes['eps_r'].value,c.attributes['t_ox'].value,c.attributes['W'].value,c.attributes['L'].value)
            self.__characteristics.append(characteristic)
        
    def parseConstants(self):
        self.__constants = dict()
        constantList = self.__xmldoc.getElementsByTagName('constant')
        for c in constantList:
            self.__constants[c.attributes['name'].value] =c.attributes['value'].value 
            
    def getConstants(self):
        return self.__constants
    
    def getTFTCharacteristics(self):
        return self.__characteristics
    
    def getConstantValue(self,name):
        return self.getConstants()[name]
    
    def getDefaultTFTNodeValues(self):
        node_values = []
        node_values.append(self.getConstantValue('vg_start'))
        node_values.append(self.getConstantValue('vg_end'))
        node_values.append(self.getConstantValue('step'))
        node_values.append(self.getConstantValue('vds'))
        
        return node_values

'''
This class represents all characteristics for one possible TFT composition.
'''
class TFTCharacteristic(object):
    
    def __init__(self,name,eps_r,t_ox,W,L):
        self.__name = name
        self.__eps_r = eps_r
        self.__tox = t_ox
        self.__W = W
        self.__L = L
    
    def getName(self):
        return self.__name
    
    def getEps_r(self):
        return self.__eps_r
    
    def getTox(self):
        return self.__tox
    
    def getW(self):
        return self.__W
    
    def getL(self):
        return self.__L
    
    def setName(self,name):
        self.__name = name
    
    def setW(self,W):
        if W <= 0:
            raise ValueError('W cannot be 0 or less')
        else:
            self.__W = W
    
    def setL(self,L):
        if L <= 0:
            raise ValueError('L cannot be 0 or less')
        else:
            self.__L = L
                
    