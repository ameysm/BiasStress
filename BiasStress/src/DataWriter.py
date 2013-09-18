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

