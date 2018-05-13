#from __future__ import absolute_import, division, print_function
from flask import Flask, render_template, jsonify, request


import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

import os

import tensorflow.contrib.eager as tfe

# Import data
data = pd.read_csv('training_set.csv')

# Drop date variable
data = data.drop(['DATE'], 1)
def trainModel(dict):
    #tf.enable_eager_execution()

    #print("TensorFlow version: {}".format(tf.VERSION))
    #print("Eager execution: {}".format(tf.executing_eagerly()))
    print(dict)