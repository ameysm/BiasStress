'''
Created on Sep 13, 2013

This class represents a wafer.

@author: Incalza Dario
'''

class Wafer(object):
    
    def __init__(self,date_code,index,proc_step,alias):
        self.__date_code = date_code
        self.__index = index
        self.__proc_step = proc_step
        self.__alias = alias
    
    def get_date_code(self):
        return str(self.__date_code)
    
    def get_index(self):
        return str(self.__index)
    
    def get_proc_step(self):
        return str(self.__proc_step)
    
    def get_relative_wafer_dir(self):
        return self.get_alias()+self.get_date_code()+"/"+self.get_index()+"/"
    
    '''
    For example : PEMD
    '''
    def get_alias(self):
        return str(self.__alias)
    
    def getWaferName(self):
        return "BIAS_"+self.get_alias()+self.get_date_code()+"_"+self.get_index()+"_"+self.get_proc_step()
  
        