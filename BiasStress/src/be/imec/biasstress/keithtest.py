'''
Created on Sep 5, 2013

@author: adminssteudel
'''

from pylab import figure,plot,linspace,show,clf,draw
from hardware.SMU import SMU

smus = [SMU(27,'A'),SMU(27,'B')]
k = 0
for smu in smus: 
    smu.reset()
    smu.set_source_type_voltage()
    smu.set_output_on()
    varray = linspace( -1, 1, 102 )

    i = []     # i and v are lists for plotting
    v = []
    for vsrc in varray:
        smu.set_output_volts( vsrc )
        v.append( vsrc )
        i.append( smu.measure_current() )
    if k == 0:
        plot(v,i,'b-')
    else:
        plot(v,i,'r-')

    draw()
    smu.reset()
    smu.close()
    k=k+1
figure(1)  # make a new plot window (or get an open one)
show()     # display it (even though it may be blank)        