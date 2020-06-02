import pandas as pd


endpoint_name = "endpoint-from-saved-model"
from sagemaker.tensorflow import TensorFlowPredictor

predictor = TensorFlowPredictor(endpoint_name)


x_test=pd.read_csv('seismic_poro_test.csv')
stats = x_test.describe()
stats.pop('porosity')
stats = stats.transpose()
x_test = (x_test - stats['mean']) / stats['std']
x_test.pop('porosity')
for a in x_test.values:
    test_predictions = predictor.predict(a)
    print(test_predictions['predictions'][0][0])