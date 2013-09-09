'''
Created on Sep 9, 2013

@author: Incalza Dario
'''

def isANumber(numberString):
    try:
        x = float(numberString)
        return True
    except ValueError:
        return False