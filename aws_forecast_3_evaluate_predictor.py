import json
import time
import dateutil.parser
import boto3
import pandas as pd
import matplotlib.pyplot as plt

predictor_arn = "arn:aws:forecast:ap-south-1:946837915266:predictor/util_power_forecastdemo_deeparp_algo"
forecast_arn =  "arn:aws:forecast:ap-south-1:946837915266:forecast/util_power_forecastdemo_deeparp_algo_forecast"

session = boto3.Session(region_name="ap-south-1")
forecast = session.client(service_name='forecast')
forecastquery = session.client(service_name='forecastquery')

forecastResponse = forecastquery.query_forecast(
    ForecastArn=forecast_arn,
    Filters={"item_id":"client_12"}
)
actual_df = pd.read_csv("item-demand-time-validation.csv", names=['timestamp','value','item'])
actual_df.head()
actual_df = actual_df[(actual_df['timestamp'] >= '2014-10-31') & (actual_df['timestamp'] < '2014-11-01')]
actual_df = actual_df[(actual_df['item'] == 'client_12')]
actual_df.head()

actual_df.plot()
prediction_df_p10 = pd.DataFrame.from_dict(forecastResponse['Forecast']['Predictions']['p10'])
prediction_df_p10.head()

prediction_df_p10.plot()

prediction_df_p50 = pd.DataFrame.from_dict(forecastResponse['Forecast']['Predictions']['p50'])
prediction_df_p90 = pd.DataFrame.from_dict(forecastResponse['Forecast']['Predictions']['p90'])

results_df = pd.DataFrame(columns=['timestamp', 'value', 'source'])
for index, row in actual_df.iterrows():
    clean_timestamp = dateutil.parser.parse(row['timestamp'])
    results_df = results_df.append({'timestamp' : clean_timestamp , 'value' : row['value'], 'source': 'actual'} , ignore_index=True)

results_df.head()
for index, row in prediction_df_p10.iterrows():
    clean_timestamp = dateutil.parser.parse(row['Timestamp'])
    results_df = results_df.append({'timestamp' : clean_timestamp , 'value' : row['Value'], 'source': 'p10'} , ignore_index=True)
for index, row in prediction_df_p50.iterrows():
    clean_timestamp = dateutil.parser.parse(row['Timestamp'])
    results_df = results_df.append({'timestamp' : clean_timestamp , 'value' : row['Value'], 'source': 'p50'} , ignore_index=True)
for index, row in prediction_df_p90.iterrows():
    clean_timestamp = dateutil.parser.parse(row['Timestamp'])
    results_df = results_df.append({'timestamp' : clean_timestamp , 'value' : row['Value'], 'source': 'p90'} , ignore_index=True)


pivot_df = results_df.pivot(columns='source', values='value', index="timestamp")
pivot_df.plot()
plt.show()