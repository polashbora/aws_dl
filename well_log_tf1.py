import tensorflow as tf
import argparse
import os
import numpy as np
import json
import pandas as pd


def model(x_train, y_train, x_test, y_test):
    """Generate a simple model"""
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])
    model.fit(x_train, y_train)
    model.evaluate(x_test, y_test)

    return model


def _load_training_data():
    x_train = pd.read_csv('well_log_train.csv')
    y_train = x_train.pop('Gamma')
    return x_train, y_train


def _load_testing_data():
    x_test = pd.read_csv('well_log_test_short.csv')
    y_test = x_test.pop('Gamma')
    return x_test, y_test


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', type=str)
    parser.add_argument('--sm-model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAINING'))
    parser.add_argument('--hosts', type=list, default=json.loads(os.environ.get('SM_HOSTS')))
    parser.add_argument('--current-host', type=str, default=os.environ.get('SM_CURRENT_HOST'))
    return parser.parse_known_args()


if __name__ == "__main__":
    args, unknown = _parse_args()
    train_data, train_labels = _load_training_data()
    eval_data, eval_labels = _load_testing_data()
    mnist_classifier = model(train_data, train_labels, eval_data, eval_labels)

    if args.current_host == args.hosts[0]:
        # save model to an S3 directory with version number '00000001'
        mnist_classifier.save(os.path.join(args.sm_model_dir, '000000001'), 'my_model.h5')