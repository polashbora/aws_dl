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
    'Inputs': ['Input1','Input2'],
}


#
# Define the compute function
#


def doCompute():
    xa.doInput()
    mylist1 = xa.Input['Input1'][0, 0, :].tolist()
    mylist2 = xa.Input['Input2'][0, 0, :].tolist()
    mylist=list(zip(mylist1,mylist2))
    myz0 = xa.TI['z0']
    myfile = open(r"C:\Users\Polash-Dell\coder_guy\PycharmProjects\snippets\123pol.csv", 'a')
    for samp in mylist:
        myfile.write(str(myz0) + ", " + str(samp[0]) + ", " + str(samp[1])+"\n")
        myz0=myz0+1
    myfile.close()

    xa.doOutput()


#
# Assign the compute function to the attribute
#
xa.doCompute = doCompute


#
# Do it
#
xa.run(sys.argv[1:])

