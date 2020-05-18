#!/usr/bin/python
#
# Calculate attributes from Inline and Crossline dip
#
#
import sys
import numpy as np

#
# Import the module with the I/O scaffolding of the External Attribute
#
import extattrib as xa

#
# These are the attribute parameters
#
xa.params = {
    'Inputs': ['Input'],
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
nrsamples = xa.TI['nrsamp'] * xa.SI['nrtraces']
myfile=open(r"C:\Users\Polash-Dell\coder_guy\PycharmProjects\snippets\123pol.txt", 'w+')
# myfile.write(str(xa.Input['Input'][0][0].tolist()))

try:
    mylist=xa.Input['Input'][0][0].tolist()
    for samp in mylist:
        myfile.write(str(samp)+"\n")
        #myfile.write("\n")
except:
    pass

myfile.close()
