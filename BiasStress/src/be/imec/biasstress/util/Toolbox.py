'''
Method signature says it all
'''

import math

def isANumber(numberString):
    try:
        x = float(numberString)
        return True
    except ValueError:
        return False

def makeTime(start, stop, points):
    result = []
    nr_decades = math.ceil(math.log10(stop))
    result.append(start)    
    for tijd in range(1, int(nr_decades)):
        for point in range(1, points + 1):
            stamp = int(10**tijd*10**(float(point)/float(points)))
            if (stamp >= 30):
                result.append(stamp)
        
    return result