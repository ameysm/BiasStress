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
        self.parseDefaultDevices()
        self.parseBiasConfig()
    
    def parseBiasConfig(self):
        self.__biasconfig = dict()
        configList = self.__xmldoc.getElementsByTagName('bias-parameter')
        for c in configList:
            self.__biasconfig[c.attributes['name'].value] =c.attributes['value'].value 
        
    def parseTftCharacteristics(self):
        characteristiclist = self.__xmldoc.getElementsByTagName('characteristic')
        self.__characteristics = [] 
        for c in characteristiclist :
            characteristic = TFTCharacteristic(c.attributes['configname'].value,c.attributes['name'].value,c.attributes['eps_r'].value,c.attributes['t_ox'].value,c.attributes['W'].value,c.attributes['L'].value)
            self.__characteristics.append(characteristic)
        
    def parseConstants(self):
        self.__constants = dict()
        constantList = self.__xmldoc.getElementsByTagName('constant')
        for c in constantList:
            self.__constants[c.attributes['name'].value] =c.attributes['value'].value 
    
    def parseDefaultDevices(self):
        self.__devices = []
        deviceList = self.__xmldoc.getElementsByTagName('device')
        for d in deviceList:
            self.__devices.append((d.attributes['node'].value,d.attributes['address'].value,d.attributes['channel'].value))
            
    def getConstants(self):
        return self.__constants
    
    def getDefaultDevices(self):
        return self.__devices
    
    def getTFTCharacteristics(self):
        return self.__characteristics
    
    def getConstantValue(self,name):
        return self.getConstants()[name]
    
    def getBiasConfig(self,parametername):
        return self.__biasconfig[parametername]
    
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
    
    def __init__(self,configname,name,eps_r,t_ox,W,L):
        self.__name = name
        self.__eps_r = eps_r
        self.__tox = t_ox
        self.__W = W
        self.__L = L
        self.__config_name = configname
        
    def getConfigName(self):
        return self.__config_name
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
            
    '''
    Necessary to override __eq__ and __ne__ in order for the lookup in lists etc to succeed on the constraints
    we would like to choose when two TFTCharacteristic instances refer to the same instance.
    '''
    def __eq__(self, other):
        if isinstance(other, TFTCharacteristic):
            return self.getName() == other.getName() and self.getConfigName() == other.getConfigName()
        
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
        
    