'''
Created on Sep 5, 2013

@author: Incalza Dario
'''
import visa

class SMU(object):

    def __init__(self,address,channel,node,device,name):
        self.__address = address
        self.__channel = channel
        self.__node = node
        self.__device = device
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


    def measure_current( self):
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


    def reset_channel( self):
        if self.__channel=='A':
            self.__device.write( "smua.reset()" )
        elif self.__channel=='B':
            self.__device.write( "smub.reset()" )
        else:
            raise ValueError("Invalid channel sent to function reset_channel")


   

    def set_current_compliance( self, compliance ):
        """ Set max output current level """
        if self.__channel=='A':
            self.__device.write( "smua.source.limiti = %s" % compliance )
        elif self.__channel=='B':
            self.__device.write( "smub.source.limiti = %s" % compliance )
        else:
            raise ValueError("Invalid channel sent to function set_current_compliance")

        
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