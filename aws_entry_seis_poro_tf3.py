import tensorflow as tf
import argparse
import os
import json
import pandas as pd


def model(x_train, y_train, x_test, y_test):
    """Generate a simple model"""
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=[1]),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])
    EPOCHS=10
    model.fit(x_train, y_train, epochs=EPOCHS, validation_split = 0.3, verbose=0)
    results=model.predict(x_test)
    print("Model has been trained\n\n")
    return model


def _load_training_data(base_dir):
    x_train = pd.read_csv(os.path.join(base_dir, 'seismic_poro_train.csv'))
    y_train=x_train.pop('porosity')
    stats = x_train.describe()
    stats = stats.transpose()
    x_train=(x_train - stats['mean']) / stats['std']
    return x_train, y_train


def _load_testing_data(base_dir):
    x_test = pd.read_csv(os.path.join(base_dir, 'seismic_poro_test.csv'))
    stats = x_test.describe()
    stats.pop('porosity')
    stats = stats.transpose()
    x_test=(x_test - stats['mean']) / stats['std']
    x_test.pop('porosity')
    y_test = (pd.read_csv(os.path.join(base_dir, 'seismic_poro_test.csv'))).pop('porosity')
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

    train_data, train_labels = _load_training_data(args.train)
    eval_data, eval_labels = _load_testing_data(args.train)

    well_log_regressor = model(train_data, train_labels, eval_data, eval_labels)

    if args.current_host == args.hosts[0]:
        # save model to an S3 directory with version number '00000001'
        well_log_regressor.save(os.path.join(args.sm_model_dir, '000000001'), 'my_model.h5')