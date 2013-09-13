'''
Created on Sep 13, 2013

@author: adminssteudel
'''
import numpy

dictdata = dict()
dictdata["0"]= numpy.random.randint(5,size=(100,3))
dictdata["31"]= numpy.random.randint(5,size=(100,3))
dictdata["56"]= numpy.random.randint(5,size=(100,3))
dictdata["100"]= numpy.random.randint(5,size=(100,3))
direction = "positive"


def writeBiasFile(dictdata,direction,total_stress,filename):
    completeName = filename
    file1 = open(completeName,"w")
    file1.write("[DATA-SCHEME = DRAIN CURRENT \t GATE CURRENT \t GATE VOLTAGE]\n")
    file1.write("[DATA-START DIRECTION='"+str(direction)+' TOTAL STRESS= '+str(total_stress)+']'+"\n")
    for key in dictdata:
        file1.write("[SWEEP ON T="+key+"]"+"\n")
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

