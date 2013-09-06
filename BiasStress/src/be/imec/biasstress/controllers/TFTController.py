'''
Created on Sep 5, 2013

@author: Incalza Dario
'''
from be.imec.biasstress.controllers.AbstractController import AbstractController
from be.imec.biasstress.models.TFT import TFT
from be.imec.biasstress.util.Logger import Logger
from be.imec.biasstress.hardware.SMU import TFT_RUN

class TFTController(AbstractController):
    
    def __init__(self,devicecontroller,ui,logger):
        AbstractController.__init__(self, devicecontroller)
        self.__ui=ui
        self.__currentTft = TFT()
        self.__logger=logger
        self.setTFTValues()
    
    def resetTFTValues(self):
        self.__ui.vgstart.setText(TFT.DEFAULT_VGS_START)
        self.__ui.vgend.setText(TFT.DEFAULT_VGS_END)
        self.__ui.vds.setText(TFT.DEFAULT_VDS)
        self.__ui.step.setText(TFT.DEFAULT_STEP)
        self.__logger.log(Logger.INFO,'TFT Values reset')

    
    def setTFTValues(self):
        self.__ui.vgstart.setText(self.__currentTft.getVgStart())
        self.__ui.vgend.setText(self.__currentTft.getVgEnd())
        self.__ui.vds.setText(self.__currentTft.getVds())
        self.__ui.step.setText(self.__currentTft.getStep())
        
    def tftRun(self):
        Vgs = int(self.__ui.vgstart.text())
        Vge = int(self.__ui.vgend.text())
        step = float(self.__ui.step.text())
        Vds = int(self.__ui.vds.text())
        gatedevice = self.getDeviceController().getDeviceMappedToNode('Vg')
        sourcedevice = self.getDeviceController().getDeviceMappedToNode('Vs')
        
        if gatedevice == None or sourcedevice == None:
            self.__logger.log(Logger.ERROR,"No devices are assigned to the gate and/or source. To be able to perform a sweep at least two devices need to be attached, node Vg and Vs need to be mapped to a channel/device")
        tftrun = TFT_RUN(gatedevice,sourcedevice)
        vgs, igs, ids = tftrun.measureTFT(Vgs, Vge, step, Vds)
        print vgs
        print igs
        print ids
        return (vgs,igs,ids)
        
        
        