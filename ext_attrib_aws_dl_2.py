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
    while True:
        xa.doInput()
        x_test_list = xa.Input['Input'][0, 0, :].tolist()
        x_test=pd.DataFrame(x_test_list)
        stats = x_test.describe()
        stats = stats.transpose()
        x_test = (x_test - stats['mean']) / stats['std']
        y_test=predictor.predict(np.array(x_test))
        xa.Output['Output']= np.array(y_test['predictions'])
        xa.doOutput()

xa.doCompute = doCompute

xa.run(sys.argv[1:])
