'''
Created on Sep 5, 2013

This class represents an AbstractController. Which means that this is a base class for other controllers and _SHOULD NOT_ be instantiated. 
Additional Controllers need to extend this class and they will have a VISA controller to handle their hardware communication.

@author: Incalza Dario
'''

class AbstractController(object):
    
    def __init__(self,visa):
        self.__visa=visa
    
    def getVisaController(self):
        return self.__visa
        