
import sys
import numpy as np
import pandas as pd
from sagemaker.tensorflow import TensorFlowPredictor



import extattrib as xa

xa.params = {
    'Inputs': ['Input'],
    'Output': ['Output']
}

def doCompute():
    endpoint_name = "endpoint-from-saved-model"

    predictor = TensorFlowPredictor(endpoint_name)

    myfile = open(r"C:\Users\Polash-Dell\coder_guy\PycharmProjects\aws_dl\1_aws_dl.txt", 'w+')
    myfile.write("Norm Amp : Porosity")
    while True:
        xa.doInput()
        x_test_list = xa.Input['Input'][0, 0, :].tolist()
        x_test=pd.DataFrame(x_test_list)
        stats = x_test.describe()
        stats = stats.transpose()
        x_test = (x_test - stats['mean']) / stats['std']
        for a in x_test.values:
            myfile.write(str(a)+": ")
            try:
                test_predictions = predictor.predict(a)
                myfile.write(str(test_predictions['predictions'][0][0])+"\n")
            except:
                e = sys.exc_info()[0]
                myfile.write("\nError:"+str(e))
        xa.Output['Output'] = xa.Input['Input']
        xa.doOutput()
    myfile.close()

xa.doCompute = doCompute

xa.run(sys.argv[1:])
