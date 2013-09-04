'''
Created on Sep 4, 2013

@author: Incalza Dario
'''
from datetime import datetime
class Logger(object):
   
    '''
    A given console that is a text widget in the gui.
    '''
    def __init__(self,console):
        self.__console = console
    '''
    Log a text to inform the user of a certain IO action. Given : the text that needs to be displayed. A timestamp will be printed before the text.
    '''
    def log(self,text):
        now = datetime.now()
        time = str(now.strftime("%H,%M")).split(",")
        time = ":".join(time)
        self.__console.append(time+" >> "+text)