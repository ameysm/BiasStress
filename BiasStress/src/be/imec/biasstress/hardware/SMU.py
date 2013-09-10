'''
Created on Sep 5, 2013

This class describes an SMU. This differs from the realistic situation in the sense that one real SMU is represented by 2 objects of this class. 
One for every channel.

@author: Incalza Dario
'''
import visa,os
from numpy.ma.core import ids

class SMU(object):
    
    NODES = dict(Vg=0x00, Vd=0x01, Vs=0x02)
    
    '''
    Creat e a new SMU by giving the address on the GPIB link, the channel, the node which the SMU controls, a device object (returned by
    the VISA lib, and the name which is obtained by sending an inquiry to the device.
    '''
    def __init__(self,address,channel,node,device,name):
        self.__address = address
        self.__channel = channel
        self.__node = node
        self.__device = device
        self.reset()
        self.__name = name
    
    def getChannel(self):
        return self.__channel
    
    def getNode(self):
        return self.__node
    
    def getDeviceId(self):
        return self.__channel+self.__address
    
    def getName(self):
        return self.__name
    
    def getAddress(self):
        return self.__address
    
    def close(self):
        """ closes the VISA instance (I think) """
        self.__device.close()

    
    def set_current_compliance( self, compliance ):
        """ Set max output current level """
        if self.__channel=='A':
            self.__device.write( "smua.source.limiti = %s" % compliance )
        elif self.__channel=='B':
            self.__device.write( "smub.source.limiti = %s" % compliance )
        else:
            raise ValueError("Invalid channel sent to function set_current_compliance")
             
    def set_voltage_compliance(self,compliance):
        """ Set max output current level """
        if self.__channel=='A':
            self.__device.write( "smua.source.limitv = %s" % compliance )
        elif self.__channel=='B':
            self.__device.write( "smub.source.limitv = %s" % compliance )
        else:
            raise ValueError("Invalid channel sent to function set_current_compliance")
        
    def measure_current(self):
        """ queries instrument, returns value """
        if self.__channel=='A':
            return self.__device.ask( "print(smua.measure.i())" )
        elif self.__channel=='B':
            return self.__device.ask( "print(smub.measure.i())" )
        else:
            raise ValueError("Invalid channel sent to function measure_current")


    def measure_voltage(self):
        """ queries instrument, returns value """
        if self.__channel=='A':
            return self.__device.ask( "print(smua.measure.v())" )
        elif self.__channel=='B':
            return self.__device.ask( "print(smub.measure.v())" )
        else:
            raise ValueError("Invalid channel sent to function measure_voltage")


    def reset(self):
        
        self.__device.write( "reset()" )
    
    def clear_buffer(self):
        if self.__channel=='A':
            self.__device.write( "smua.nvbuffer1.clear()" )
        elif self.__channel=='B':
            self.__device.write( "smub.nvbuffer1.clear()" )
        else:
            raise ValueError("Invalid channel sent to function reset_channel")

    def reset_channel( self):
        if self.__channel=='A':
            self.__device.write( "smua.reset()" )
        elif self.__channel=='B':
            self.__device.write( "smub.reset()" )
        else:
            raise ValueError("Invalid channel sent to function reset_channel")

        
    def set_output_on( self):
        """ turn on output """
        if self.__channel=='A':
            self.__device.write( "smua.source.output = smua.OUTPUT_ON" )
        elif self.__channel=='B':
            self.__device.write( "smub.source.output = smub.OUTPUT_ON" )
        else:
            raise ValueError("Invalid channel sent to function set_output_on")

        
    def set_output_off( self):
        """ turn off output """
        if self.__channel=='A':
            self.__device.write( "smua.source.output = smua.OUTPUT_OFF" )
        elif self.__channel=='B':
            self.__device.write( "smub.source.output = smub.OUTPUT_OFF" )
        else:
            raise ValueError("Invalid channel sent to function set_output_off")

        
    def set_output_amps( self, amps ):
        """ set the output current in amps """
        if self.__channel=='A':
            self.__device.write( "smua.source.leveli = %s" % amps )
        elif self.__channel=='B':
            self.__device.write( "smub.source.leveli = %s" % amps )
        else:
            raise ValueError("Invalid channel sent to function set_output_amps")

        
    def set_output_volts( self, volts ):
        """ set the output voltage level in volts """
        if self.__channel=='A':
            self.__device.write( "smua.source.levelv = %s" % volts )
        elif self.__channel=='B':
            self.__device.write( "smub.source.levelv = %s" % volts )
        else:
            raise ValueError("Invalid channel sent to function set_output_volts")

        
    def set_source_type_current( self, src_range=None):
        """
        set the smu channel to source current (in amps)
        if `src_range` is not specified, smu source will be set to autorange
        """
        if self.__channel=='A':
            self.__device.write( "smua.source.func = smua.OUTPUT_DCAMPS" )
            if src_range is None:
                self.__device.write(  "smua.source.autorangei = smua.AUTORANGE_ON" )
            else:                         
                self.__device.write(  "smua.source.rangev = %s" % src_range )
        elif self.__channel=='B':
            self.__device.write( "smub.source.func = smub.OUTPUT_DCAMPS" )
            if src_range is None:
                self.__device.write(  "smub.source.autorangei = smub.AUTORANGE_ON" )
            else:                         
                self.__device.write(  "smub.source.rangev = %s" % src_range )
        else:
            raise ValueError("Invalid channel sent to function set_source_type_current")


    def set_source_type_voltage( self, src_range=None):
        """
        set the smu channel to source volts
        if `src_range` is not specified, smu source will be set to autorange
        """
        if self.__channel=='A':
            self.__device.write( "smua.source.func = smua.OUTPUT_DCVOLTS" )
            if src_range is None:
                self.__device.write(  "smua.source.autorangev = smua.AUTORANGE_ON" )
            else:                         
                self.__device.write(  "smua.source.rangev = %s" % src_range )
        elif self.__channel=='B':
            self.__device.write( "smub.source.func = smub.OUTPUT_DCVOLTS" )
            if src_range is None:
                self.__device.write(  "smub.source.autorangev = smub.AUTORANGE_ON" )
            else:                         
                self.__device.write(  "smub.source.rangev = %s" % src_range )
        else:
            raise ValueError("Invalid channel sent to function set_source_type_voltage")
        
    def write( self, command_string ):
        """ send the supplied string to the instrument """
        self.__device.write( command_string )
    
    '''
    Necessary to override __eq__ and __ne__ in order for the lookup in lists etc to succeed on the constraints
    we would like to choose when two SMU instances refer to the same instance.
    '''
    def __eq__(self, other):
        if isinstance(other, SMU):
            return self.getName() == other.getName() and self.getAddress() == other.getAddress() and self.getChannel() == other.getChannel()
        
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    
    def read(self):
        self.__device.timeout = 60
        return self.__device.read()
    
    def loadandRunScriptfromFile(self, scriptFilePath):
        scriptName, fileExtension = os.path.splitext(scriptFilePath)
        f = file(scriptFilePath, "r")
        flines = f.readlines()
        f.close()
        flines = "".join(flines)        
        script = "loadandrunscript " + scriptName + "\n" + flines + "\n" + "endscript"
        del self.__device.timeout
        self.__device.write(script)
        return script

    def readBuffer(self, whichBuffer = "nvbuffer1", startIndex = 1, stopIndex = 1, split = ","):
    
        # !This is the formated string! Good to know.----Xuanwu
        # !Be careful of the Tuple style (single,)
        readBufferCommand = "printbuffer( %d,%d,%s.%s)" % (startIndex, stopIndex, self.getChannelAsScriptVariable(), whichBuffer)
        self.__device.write(readBufferCommand)
        readout = self.__device.read()
        readout = readout.split(",")
        return readout
    
    def getChannelAsScriptVariable(self):
        channel = self.getChannel().lower()
        return 'smu'+channel
    
    def loadScript(self,scriptfile):
        f = file(scriptfile.getPath, "r")
        flines = f.readlines()
        f.close()
        flines = "".join(flines)    
        script = "loadscript " + scriptfile.getName() + "\n" + flines + "\n" + "endscript"
        self.__device.write(script)
    
    

class TFT_RUN(object):
    def __init__(self,gatedevice,sourcedevice):
        self.smu_gd = gatedevice
        self.smu_s = sourcedevice
            
    def __del__(self):
        pass
    
    def inList(self,tools, addr):
        count = 0
        nr_tools = len(tools)
        while (count < nr_tools):
            if len(tools[count]) > 7:
                cur_addr = int(tools[count][7:])
                if cur_addr == addr:
                    return 1
            count = count + 1
        return 0  
    
    def makeFloat(self,vlist, ab):
        temp = []
        for i in range(0, len(vlist)):
            if ab:
                temp.append(abs(float(vlist[i])))
            else:
                temp.append(float(vlist[i]))
        return temp
    
    def display(self, sel):
        if sel == 'Amps':
            func = 'display.MEASURE_DCAMPS'
        elif sel == 'Volt':
            func = 'display.MEASURE_DCVOLTS'
        elif sel == 'Ohms':
            func = 'display.MEASURE_OHMS'
        elif sel == 'Watt':
            func = 'display.MEASURE_WATTS'
                
        script = 'display.smua.measure.func=' + func + '\ndisplay.smub.measure.func=' + func + '\n'
        self.Write(script)
    
    def reset(self):
        script = 'smua.reset()\nsmub.reset()\nerrorqueue.clear()'
        self.Write(script)
    
    def init(self):
        print 'Devices found:'
        print self.smu_gd.askIDN()
        print self.smu_s.askIDN()    
        self.reset()        
            
    def Open(self):
        tools = visa.get_instruments_list()
        if self.inList(tools, 26) & self.inList(tools, 27):
            #tools are found, now we can open them

            if self.smu_gd.Open(27) & self.smu_s.Open(26):
                self.init()
            else:
                print 'Error opening tools!'
                    
        else:
            print 'Tools not found!'
            return -1
            
    def Close(self):
        self.smu_gd.Close()
        self.smu_s.Close()
        
    def Write(self, script):
        self.smu_gd.write(script)
        self.smu_s.write(script)
        
    def Source(self, mode):
        if mode == 'Amps':
            func = '0'
        elif mode == 'Volts':
            func = '1'
            
        script = 'smua.source.func=' + func + '\nsmub.source.func=' + func + '\n'
        self.Write(script)
        
    def setBuffers(self):
        script = 'smua.nvbuffer1.clear()\nsmub.nvbuffer1.clear()\nsmua.nvbuffer1.appendmode = 1\nsmub.nvbuffer1.appendmode = 1'
        self.Write(script)
        
    def setVLimit(self, lim):
        script = 'smua.source.limitv=' + str(lim) + '\nsmub.source.limitv' + str(lim) + '\n'
        self.Write(script)
        
    def setILimit(self, lim):
        script = 'smua.source.limiti=' + str(lim/1000) + '\nsmub.source.limiti=' + str(lim/1000) + '\n'
        self.Write(script)
        
    def setVd(self, vd):
        script = 'smub.source.levelv=' + str(vd) + '\n'
        self.smu_gd.write(script)
        script = 'smub.source.levelv=0'
        self.smu_s.write(script)
        
    def setOutput(self, mode):
        if mode == 'on':
            func = '1'
        elif mode == 'off':
            func = '0'
        elif mode == 'high':
            func = '2'
        script = 'smua.source.output=' + func + ' smub.source.output=' + func
        self.Write(script) 
        
    def sweepGate(self, start, stop, step):
        punten = int(abs(stop-start) / step ) + 1
        vgs = []
        for i in range(0,punten):
            gate = start + i * step
            vgs.append(gate)
        
        script = 'for x = 1, ' + str(punten) + ' do smua.source.levelv = ' + str(start) + ' + x * ' + str(step) + ' delay(0.05) smua.measure.i(smua.nvbuffer1)  smub.measure.i(smub.nvbuffer1) waitcomplete() end count=smua.nvbuffer1.n print("OK", count)'        
        self.setOutput('on')
        self.smu_gd.write(script)
        readout = self.smu_gd.read()
        readings = int(float(readout.split('\t')[1]))
        self.setOutput('off')
        igs = self.smu_gd.readBuffer('smua', 'nvbuffer1', 1, readings)
        ids = self.smu_gd.readBuffer('smub', 'nvbuffer1', 1, readings)
        return vgs, igs, ids
        
    def setBias(self, vg, vd):
        script = 'smua.source.levelv=' + str(vg) + '\nsmub.source.levelv=' + str(vd) + '\n'
        self.smu_gd.write(script)
        script = 'smub.source.levelv=0'
        self.smu_s.write(script)
        self.setOutput('on')
         
    def measureTFT(self, start, stop, step, vd):
        self.reset()
        self.setBuffers()
        self.display('Amps')
        self.Source('Volts')
        self.setILimit(100.0)
        self.setVd(vd)
        vgs, igs, ids = self.sweepGate(start, stop, step)
        ids = self.makeFloat(ids, 1)
        igs = self.makeFloat(igs, 1)
        vgs = self.makeFloat(vgs, 0)
        return vgs, igs, ids