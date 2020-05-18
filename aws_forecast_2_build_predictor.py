import time
import boto3


datasetGroupArn="arn:aws:forecast:ap-south-1:946837915266:dataset-group/util_power_forecastdemo_dsg"
datasetArn="arn:aws:forecast:ap-south-1:946837915266:dataset/util_power_forecastdemo_ds"
role_name = "ForecastRoleDemo"
key="item-demand-time.csv"
bucket_name="forecastdemopolashbora"
region="ap-south-1"
DatasetImportJobArn="arn:aws:forecast:ap-south-1:946837915266:dataset-import-job/util_power_forecastdemo_ds/EP_DSIMPORT_JOB_TARGET"
project = 'util_power_forecastdemo'



session = boto3.Session(region_name=region)
forecast = session.client(service_name='forecast')
forecastquery = session.client(service_name='forecastquery')

predictorName= project+'_deeparp_algo'
forecastHorizon = 24

algorithmArn = 'arn:aws:forecast:::algorithm/Deep_AR_Plus'


create_predictor_response=forecast.create_predictor(PredictorName=predictorName,
                                                  AlgorithmArn=algorithmArn,
                                                  ForecastHorizon=forecastHorizon,
                                                  PerformAutoML= False,
                                                  PerformHPO=False,
                                                  EvaluationParameters= {"NumberOfBacktestWindows": 1,
                                                                         "BackTestWindowOffset": 24},
                                                  InputDataConfig= {"DatasetGroupArn": datasetGroupArn},
                                                  FeaturizationConfig= {"ForecastFrequency": "H",
                                                                        "Featurizations":
                                                                        [
                                                                          {"AttributeName": "target_value",
                                                                           "FeaturizationPipeline":
                                                                            [
                                                                              {"FeaturizationMethodName": "filling",
                                                                               "FeaturizationMethodParameters":
                                                                                {"frontfill": "none",
                                                                                 "middlefill": "zero",
                                                                                 "backfill": "zero"}
                                                                              }
                                                                            ]
                                                                          }
                                                                        ]
                                                                       }
                                                 )
predictor_arn=create_predictor_response['PredictorArn']
print("predictor_arn = ",predictor_arn)

while True:
    status = forecast.describe_predictor(PredictorArn=predictor_arn)['Status']
    if status in ('ACTIVE', 'CREATE_FAILED'): break
    time.sleep(10)

print(forecast.get_accuracy_metrics(PredictorArn=predictor_arn))
forecastName= project+'_deeparp_algo_forecast'
create_forecast_response=forecast.create_forecast(ForecastName=forecastName,
                                                  PredictorArn=predictor_arn)
forecast_arn = create_forecast_response['ForecastArn']
print("forecast_arn = ",forecast_arn)
while True:
    status = forecast.describe_forecast(ForecastArn=forecast_arn)['Status']
    if status in ('ACTIVE', 'CREATE_FAILED'): break
    time.sleep(10)
print()
forecastResponse = forecastquery.query_forecast(
    ForecastArn=forecast_arn,
    Filters={"item_id":"client_12"}
)
print(forecastResponse)

print()
forecastResponse = forecastquery.query_forecast(
    ForecastArn=forecast_arn,
    Filters={"item_id":"client_12"}
)
print(forecastResponse)
