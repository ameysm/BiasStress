'''
Created on Sep 13, 2013

This class represents a packet with Biasdata. 

@author: Incalza Dario
'''

class BiasPacket(object):

    def __init__(self,ig_list,id_list,v_list):
        self.__ig_list = ig_list
        self.__id_list = id_list
        self.__v_list =v_list
        
    def getVoltageList(self):
        return self.__v_list
    
    def getDrainList(self):
        return self.__id_list
    
    def getGateList(self):
        return self.__ig_list
    
    def get_extra_info(self):
        return self.__extra_info
    
    
