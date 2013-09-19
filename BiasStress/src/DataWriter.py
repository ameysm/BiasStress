'''
Created on Sep 13, 2013

@author: Incalza Dario
'''

'''
This function enables us to write bias data to a file.
@param dictdata: is a dictionary structure with timestamps of sweeps as key and a biaspacket containing the measurement data as value
@param total_stress: is the total_stress time that was used to measure the TFT
@param filename: A given filename under which the file should be saved
'''
from Logger import Logger
def writeBiasFile(extrainfo,dictdata,direction,total_stress,filename):
    completeName = filename
    file1 = open(completeName,"w")
    file1.write("##################### EXTRA INFO ########################\n")
    for key in extrainfo:
        file1.write(key+" = "+extrainfo[key]+"\n")
    file1.write("################### END EXTRA INFO ######################\n")
    file1.write("[DATA-SCHEME = DRAIN CURRENT \t GATE CURRENT \t GATE VOLTAGE]\n")
    file1.write("[DATA-START DIRECTION= "+str(direction)+" TOTAL STRESS= "+str(total_stress)+']'+"\n")
    for key in dictdata:
        file1.write("[SWEEP ON T= "+key+" ]"+"\n")
        biasdata = dictdata[key]
        d = biasdata.getDrainList()
        g = biasdata.getGateList()
        v = biasdata.getVoltageList()
        i = 0
        while i < len(d) :
            file1.write(str(d[i])+"\t"+str(g[i])+"\t"+str(v[i])+"\n")
            i=i+1
        file1.write("[SWEEP END]"+"\n")
    file1.write("[DATA-END]")
    file1.close()

class BiasFileWriter(object):
    
    def __init__(self,path,logger):
        self.__path = path
        self.__logger = logger
    '''
    Write the header of a .bias data file
    '''
    def writeHeader(self,extrainfo,direction,total_stress):
        try:
            myfile = open(self.__path,"w")
            myfile.write("##################### EXTRA INFO ########################\n")
            for key in extrainfo:
                myfile.write(key+" = "+extrainfo[key]+"\n")
            myfile.write("################### END EXTRA INFO ######################\n")
            myfile.write("[DATA-SCHEME = DRAIN CURRENT \t GATE CURRENT \t GATE VOLTAGE]\n")
            myfile.write("[DATA-START DIRECTION= "+str(direction)+" TOTAL STRESS= "+str(total_stress)+']'+"\n")
            myfile.write("[DATA-END]")
            myfile.close()
            self.__logger.log(Logger.INFO,"Bias data file created at "+str(self.__path))
        except OSError:
            raise
    '''
    Append sweep data to the .bias file
    '''
    def appendSweepData(self,timestamp,biasdata):
        try:
            myfile = open(self.__path,"r")
            lines = myfile.readlines()
            myfile.close()
            myfile = open(self.__path,"w")
            myfile.writelines([item for item in lines[:-1]])
            myfile.write("[SWEEP ON T= "+timestamp+" ]"+"\n")
            d = biasdata.getDrainList()
            g = biasdata.getGateList()
            v = biasdata.getVoltageList()
            i = 0
            while i < len(d) :
                myfile.write(str(d[i])+"\t"+str(g[i])+"\t"+str(v[i])+"\n")
                i=i+1
            myfile.write("[SWEEP END]"+"\n")
            myfile.write("[DATA-END]")
            myfile.close()
            self.__logger.log(Logger.INFO,"Appended sweep data at "+str(self.__path))
        except OSError:
            raise
            
