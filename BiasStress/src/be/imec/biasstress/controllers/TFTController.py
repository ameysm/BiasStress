'''
Created on Sep 5, 2013

@author: Incalza Dario
'''
from be.imec.biasstress.controllers.AbstractController import AbstractController
from be.imec.biasstress.models.TFT import TFT
from be.imec.biasstress.util.Logger import Logger

class TFTController(AbstractController):
    
    def __init__(self,visacontroller,ui,logger):
        AbstractController.__init__(self, visacontroller)
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
        