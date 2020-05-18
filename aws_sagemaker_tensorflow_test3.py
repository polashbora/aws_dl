import numpy as np
import pandas as pd
import sagemaker
from sagemaker.predictor import csv_serializer, json_deserializer


endpoint_name = "tensorflow-training-2020-05-17-15-11-17-715"
from sagemaker.tensorflow import TensorFlowPredictor

predictor = TensorFlowPredictor(endpoint_name)

x_test = pd.read_csv('seismic_poro_test.csv')
stats = x_test.describe()
stats.pop('porosity')
stats = stats.transpose()
x_test = (x_test - stats['mean']) / stats['std']
x_test.pop('porosity')
for a in x_test.as_matrix():
    test_predictions = predictor.predict(a)
    print(test_predictions['predictions'][0][0])
