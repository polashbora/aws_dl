import sagemaker
import numpy as np
from sagemaker.tensorflow import TensorFlow




sagemaker_session = sagemaker.Session()

role = 'sagemaker_full_role'
region = sagemaker_session.boto_session.region_name
training_data_uri = 's3://forecastdemopolashbora/tensorflow/'


estimator = TensorFlow(entry_point='aws_entry_seis_poro_tf2.py',
                             role=role,
                             train_instance_count=2,
                             train_instance_type='ml.c4.2xlarge',
                             framework_version='2.1.0',
                             py_version='py3',
                             distributions={'parameter_server': {'enabled': True}})

estimator.fit(training_data_uri)