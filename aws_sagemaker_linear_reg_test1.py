import numpy as np
import pandas as pd
import sagemaker


endpoint_name = "polash-sagemaker-regression-v1"  # Your endpoint name.

predictor = sagemaker.predictor.RealTimePredictor(endpoint_name)

from sagemaker.predictor import csv_serializer, json_deserializer

predictor.content_type = 'text/csv'
predictor.serializer = csv_serializer
predictor.deserializer = json_deserializer



test_dataset = pd.read_csv("well_log_test_short.csv")
test_feature_dataset = test_dataset[['Density', 'Sonic']]
test_features = np.array(test_feature_dataset.values).astype('float32')
prediction = predictor.predict(test_features)

mylist=[]
for a in (prediction['predictions']):
    mylist.append(a['score'])

mydf=pd.DataFrame(mylist,columns=['Comp_Gamma'])
df_col = pd.concat([test_dataset,mydf], axis=1)
print(df_col)

