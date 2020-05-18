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
    'Inputs': ['Input'],
}


#
# Define the compute function
#


def doCompute():
    xa.doInput()
    mylist = xa.Input['Input'][0, 0, :].tolist()
    myz0 = xa.TI['z0']
    myfile = open(r"C:\Users\Polash-Dell\coder_guy\PycharmProjects\snippets\321pol.csv", 'a')
    for samp in mylist:
        myfile.write(str(myz0) + ", " + str(samp) + "\n")
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

