import sagemaker
import numpy as np
from sagemaker.tensorflow import TensorFlow




sagemaker_session = sagemaker.Session()

role = 'sagemaker_full_role'
region = sagemaker_session.boto_session.region_name
print(region)
training_data_uri = 's3://sagemaker-sample-data-{}/tensorflow/mnist'.format(region)


mnist_estimator2 = TensorFlow(entry_point='mnist-2.py',
                             role=role,
                             train_instance_count=2,
                             train_instance_type='ml.c4.2xlarge',
                             framework_version='2.1.0',
                             py_version='py3',
                             distributions={'parameter_server': {'enabled': True}})

mnist_estimator2.fit(training_data_uri)
predictor2 = mnist_estimator2.deploy(initial_instance_count=1, instance_type='ml.c4.2xlarge')


train_data = np.load('train_data.npy')
train_labels = np.load('train_labels.npy')

predictions2 = predictor2.predict(train_data[:50])
for i in range(0, 50):
    prediction = predictions2['predictions'][i]
    label = train_labels[i]
    print('prediction is {}, label is {}, matched: {}'.format(prediction, label, prediction == label))


sagemaker.Session().delete_endpoint(predictor2.endpoint)
