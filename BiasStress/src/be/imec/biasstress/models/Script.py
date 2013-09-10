'''
Created on Sep 6, 2013

@author: Incalza Dario
'''

class Script(object):
    '''
    classdocs
    '''


    def __init__(self,name,path,size):
        self.__name = name
        self.__path = path
        self.__size = size
    
    def getSize(self):
        return str(self.__size)
    
    def getName(self):
        return self.__name
    
    def getPath(self):
        return self.__path
    
    
    '''
    Necessary to override __eq__ and __ne__ in order for the lookup in lists etc to succeed on the constraints
    we would like to choose when two Script instances refer to the same instance.
    '''
    def __eq__(self, other):
        if isinstance(other, Script):
            return self.getName() == other.getName() and self.getPath() == other.getPath() and self.getSize() == other.getSize()
        
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
        