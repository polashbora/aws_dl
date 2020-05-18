#!/usr/bin/python
#
# Calculate attributes from Inline and Crossline dip
#
#
import sys
import numpy as np
import pandas as pd

#
# Import the module with the I/O scaffolding of the External Attribute
#
import extattrib as xa

#
# These are the attribute parameters
#
xa.params = {
    'Inputs': ['Input','Input1'],
    'Output': ['Output'],
    'Help': 'http://waynegm.github.io/OpendTect-Plugin-Docs/external_attributes/DipandAzimuth.html'
}


#
# Define the compute function
#
def doCompute():
    while True:
        xa.doInput()

        #
        #	Get the output
        xa.Output['Output'] = xa.Input['Input'] * 5
        xa.doOutput()


#
# Assign the compute function to the attribute
#
xa.doCompute = doCompute
#
# Do it
#
xa.run(sys.argv[1:])

try:
    mylist=xa.Input['Input'][0][0]
    mylist1=xa.Input['Input1'][0][0]
    #flist=np.concatenate(mylist,mylist1)
    #np.savetxt('myfile.txt', (x, y, z), fmt='%.18g', delimiter=' ', newline=os.linesep)

    np.savetxt(r"C:\Users\Polash-Dell\coder_guy\PycharmProjects\snippets\1234pol.csv", np.c_[mylist, mylist1], delimiter=',', fmt='%20.10f', header='Porosity,Amplitude')



except:
    pass

