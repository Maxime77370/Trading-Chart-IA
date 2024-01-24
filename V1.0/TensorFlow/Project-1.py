# installation des packages
import numpy as np 
import csv
import tensorflow as tf 
import pandas as pd
from collections import namedtuple
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os
import datetime
from os.path import dirname, exists, expanduser, isdir, join, splitext

bars = pd.read_csv('AUD-CAD.csv')

print(bars.shape)

X = bars.copy()
Y = X.pop('evo')

print(X.head())

scaler = StandardScaler()

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 1)

# construction de réseaux de nerone
model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Dense(units = 13, activation = 'relu', kernel_initializer = 'uniform', input_dim = 18))
model.add(tf.keras.layers.Dense(units = 13, activation = 'sigmoid', kernel_initializer = 'uniform'))
model.add(tf.keras.layers.Dense(units = 1, activation = 'sigmoid', kernel_initializer = 'uniform'))

model.summary()

model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['binary_accuracy'])

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.fit(X_train, Y_train, epochs = 200, callbacks=[tensorboard_callback])

test_loss, test_accuracy = model.evaluate(X_test, Y_test)
print(f'Test accuracy {test_accuracy} et test loss {test_loss}')