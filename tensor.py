#from __future__ import absolute_import, division, print_function
from flask import Flask, render_template, jsonify, request


import os
import matplotlib.pyplot as plt
import numpy as np

#import tensorflow as tf
#import tensorflow.contrib.eager as tfe

def trainModel(dict):
    #tf.enable_eager_execution()

    #print("TensorFlow version: {}".format(tf.VERSION))
    #print("Eager execution: {}".format(tf.executing_eagerly()))
    print(dict)