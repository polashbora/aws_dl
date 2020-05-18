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
    while True:
        xa.doInput()
        mylist=xa.Input['Input'][0, 0, :].tolist()
        myfile = open(r"C:\Users\Polash-Dell\coder_guy\PycharmProjects\snippets\123pol.txt", 'a')
        myfile.write(str(xa.TI['z0'])+"\n"+str(mylist)+"\n")
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

# myhead=str(xa.TI['nrsamp'])+ " " + str(xa.TI['inl'])+ " " + str(xa.TI['crl'])
# np.savetxt(r"C:\Users\Polash-Dell\coder_guy\PycharmProjects\snippets\1234pol.csv", mylist, delimiter=',', fmt='%20.10f', header=myhead)
