# -*- coding: utf-8 -*-
"""Digit Recognizer CNN V2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UhYBRlfaX3c3NkP0OjPMFPzUc7xIKn5d

This notebook is representative of my submission to the Digit Recognizer Kaggle Competiton.

##Pre-Process Data
"""

import urllib
import numpy as np 
import pandas as pd 
import re
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

df = pd.read_csv('train.csv')
print(df.shape)

y =  df.pop('label').values
print(f"y is {y} and shape is {y.shape}")

X = df[:].values

def split_data(X, y, TRAIN_SIZE, TEST_SIZE, VAL_SIZE):
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=TEST_SIZE, stratify=y, shuffle=SHUFFLE)
  X_train, X_val, y_train, y_val = train_test_split(
      X_train, y_train, test_size=VAL_SIZE, stratify=y_train, shuffle=SHUFFLE)  
  return X_train, X_test, X_val, y_train, y_test, y_val

TRAIN_SIZE = 0.7
TEST_SIZE = 0.15
VAL_SIZE = 0.15
SHUFFLE = True

#Creating Data Splits 
X_train, X_test, X_val, y_train, y_test, y_val = split_data(X, y, TRAIN_SIZE, TEST_SIZE, VAL_SIZE)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

"""##Tokenize and Create Tokens"""

from sklearn.preprocessing import LabelEncoder
y_tokenizer = LabelEncoder()
y_tokenizer = y_tokenizer.fit(y_train)

y_train = y_tokenizer.transform(y_train)
y_test = y_tokenizer.transform(y_test)
y_val = y_tokenizer.transform(y_val)
classes = y_tokenizer.classes_
print(f"classes are {classes}")

"""##Create CNN Model"""

from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import GlobalMaxPool2D
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model
from tensorflow.keras.utils import plot_model
from tensorflow.keras.layers import Input
import tensorflow as tf

FILTER_SIZE = 10
NUM_CLASSES = len(classes)
print(NUM_CLASSES)
HIDDEN_DIM = 256
DROPOUT_P = 0.1

class CNN(Model):
  def __init__(self, num_classes, filter_size, hidden_dim):
    super(CNN, self).__init__(name='cnn')

    self.num_classes = num_classes
    self.filter_size = filter_size

    #Create Convolutional Filters
    self.conv = Conv2D(filters=filter_size, kernel_size=(28,28), padding='same', activation='relu')
    self.relu = Activation(activation='relu')
    self.batch_norm = BatchNormalization()
    self.pool = GlobalMaxPool2D(data_format='channels_last')

    #Create FC layers
    self.fc1 = Dense(units=hidden_dim, activation='relu')
    self.Dropout = Dropout(rate=DROPOUT_P)
    self.fc2 = Dense(units=num_classes, activation='softmax')


  def call(self, X_in, training=False):
    
    X_in = tf.cast(X_in, tf.float32)

    z = self.conv(X_in)
    z = self.relu(z)
    z = self.batch_norm(z)
    z = self.pool(z)

    z = self.fc1(z)
    z = self.Dropout(z, training=training)
    y_pred = self.fc2(z)

    return y_pred

  def summary(self, input_shape):
      x_in = Input(shape=input_shape, name='X')
      summary = Model(inputs=x_in, outputs=self.call(x_in), name=self.name)
      return plot_model(summary, show_shapes=True) # forward pass

model = CNN(
    num_classes=NUM_CLASSES,
    filter_size=FILTER_SIZE,
    hidden_dim=HIDDEN_DIM
)

X_train = X_train.reshape((X_train.shape[0], 28, 28, 1))
X_test = X_test.reshape((X_test.shape[0], 28, 28, 1))
X_val = X_val.reshape((X_val.shape[0], 28, 28, 1))
print(X_train.shape)

model.summary(input_shape=(28,28,1))

"""##Train Model"""

# Commented out IPython magic to ensure Python compatibility.
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy
from tensorflow.keras.optimizers import Adam
# %load_ext tensorboard
LEARNING_RATE = 1e-3
EARLY_STOPPING_CRITERIA = 3
NUM_EPOCHS = 50

# Compile
model.compile(optimizer=Adam(lr=LEARNING_RATE),
              loss=SparseCategoricalCrossentropy(),
              metrics=[SparseCategoricalAccuracy()])

# Callbacks
callbacks = [EarlyStopping(monitor='val_loss', patience=EARLY_STOPPING_CRITERIA, verbose=1, mode='min'),
             ReduceLROnPlateau(patience=1, factor=0.1, verbose=0),
             TensorBoard(log_dir='tensorboard', histogram_freq=1, update_freq='epoch')]

# Training
training_history = model.fit(x=X_train, y=y_train,
                             epochs=NUM_EPOCHS,
                             validation_data=(X_test, y_test), 
                             callbacks=callbacks,
                             batch_size=64,
                             verbose=1)



"""##Validation Data"""

def get_performance(y_true, y_pred, classes):
    """Per-class performance metrics. """
    performance = {'overall': {}, 'class': {}}
    y_pred = np.argmax(y_pred, axis=1)
    metrics = precision_recall_fscore_support(y_true, y_pred)

    # Overall performance
    performance['overall']['precision'] = np.mean(metrics[0])
    performance['overall']['recall'] = np.mean(metrics[1])
    performance['overall']['f1'] = np.mean(metrics[2])
    performance['overall']['num_samples'] = np.float64(np.sum(metrics[3]))

    # Per-class performance
    for i in range(len(classes)):
        performance['class'][classes[i]] = {
            "precision": metrics[0][i],
            "recall": metrics[1][i],
            "f1": metrics[2][i],
            "num_samples": np.float64(metrics[3][i])
        }

    return performance

# Evaluation
test_history = model.evaluate(x=X_val, y=y_val, verbose=1)
y_pred_val = model.predict(x=X_val, verbose=1)
print (f"test history: {test_history}")

"""##Submission"""

test_df = pd.read_csv('test.csv')
X_predict = test_df.to_numpy()
X_predict = X_predict.reshape((X_predict.shape[0], 28, 28, 1))
y_predict = model.predict(x=X_predict, verbose=1)
predicted_values = np.array(tf.argmax(y_predict, axis=1))

my_submission = pd.DataFrame({'ImageId': list(range(1, len(predicted_values)+1)), 'Label': predicted_values})

my_submission.to_csv('submission.csv', index=False)