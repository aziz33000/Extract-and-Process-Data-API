#from __future__ import absolute_import, division, print_function
from flask import Flask, render_template, jsonify, request


import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


import os
import csv
#import tensorflow.contrib.eager as tfe


def trainModel(dict):
        
    data = pd.read_csv('ENSIStage_DataMinning.csv', delimiter=';')

    # Drop
    data.drop('EmployeeNumber', axis=1, inplace=True)
    data.drop('Department', axis=1, inplace=True)
    data.drop('EducationField', axis=1, inplace=True)
    data.drop('Gender', axis=1, inplace=True)
    data.drop('JobRole', axis=1, inplace=True)
    data.drop('Over18', axis=1, inplace=True)

    n = data.shape[0]
    p = data.shape[1]

    #Attrition	MonthlyIncome	DistanceFromHome	YearsAtCompany	BusinessTravel
    data = data.values

    train_start = 0
    train_end = int(np.floor(0.8*n))
    test_start = train_end
    test_end = n
    data_train = data[np.arange(train_start, train_end), :]
    data_test = data[np.arange(test_start, test_end), :]

    #scaling
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    scaler.fit(data_train)
    data_train = scaler.transform(data_train)
    data_test = scaler.transform(data_test)
    # Build X and y
    X_train = data_train[:, 1:]
    y_train = data_train[:, 0]
    X_test = data_test[:, 1:]
    y_test = data_test[:, 0]


    ##########################################
    n_employee = data_train.shape[1]

    # Placeholder
    X = tf.placeholder(dtype=tf.float32, shape=[None, n_employee])  #Attrition	MonthlyIncome	DistanceFromHome	YearsAtCompany	BusinessTravel
    Y = tf.placeholder(dtype=tf.float32, shape=[None])

    # Model architecture parameters
    n_neurons_1 = 512 # 5 times the output
    n_neurons_2 = 256
    n_neurons_3 = 128
    n_neurons_4 = 64
    n_target = 1

    # Sessio    n
    net = tf.InteractiveSession()


    # Initializers
    sigma = 1
    weight_initializer = tf.variance_scaling_initializer(mode="fan_avg", distribution="uniform", scale=sigma)
    bias_initializer = tf.zeros_initializer()

    # Layer 1
    W_hidden_1 = tf.Variable(weight_initializer([n_employee, n_neurons_1]))
    bias_hidden_1 = tf.Variable(bias_initializer([n_neurons_1]))
    # Layer 2
    W_hidden_2 = tf.Variable(weight_initializer([n_neurons_1, n_neurons_2]))
    bias_hidden_2 = tf.Variable(bias_initializer([n_neurons_2]))
    # Layer 3
    W_hidden_3 = tf.Variable(weight_initializer([n_neurons_2, n_neurons_3]))
    bias_hidden_3 = tf.Variable(bias_initializer([n_neurons_3]))
    # Layer 4
    W_hidden_4 = tf.Variable(weight_initializer([n_neurons_3, n_neurons_4]))
    bias_hidden_4 = tf.Variable(bias_initializer([n_neurons_4]))

    # Output layer
    W_out = tf.Variable(weight_initializer([n_neurons_4, n_target]))
    bias_out = tf.Variable(bias_initializer([n_target]))


    # Hidden layer
    hidden_1 = tf.nn.relu(tf.add(tf.matmul(X, W_hidden_1), bias_hidden_1))
    hidden_2 = tf.nn.relu(tf.add(tf.matmul(hidden_1, W_hidden_2), bias_hidden_2))
    hidden_3 = tf.nn.relu(tf.add(tf.matmul(hidden_2, W_hidden_3), bias_hidden_3))
    hidden_4 = tf.nn.relu(tf.add(tf.matmul(hidden_3, W_hidden_4), bias_hidden_4))

    # Output layer (must be transposed)
    out = tf.transpose(tf.add(tf.matmul(hidden_4, W_out), bias_out))

    # Cost function
    mse = tf.reduce_mean(tf.squared_difference(out, Y))

    # Optimizer
    opt = tf.train.AdamOptimizer().minimize(mse)

    # Init
    net.run(tf.global_variables_initializer())

    # Setup plot
    plt.ion()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    line1, = ax1.plot(y_test)
    line2, = ax1.plot(y_test * 0.5)
    plt.show()

    # Fit neural net
    batch_size = 64
    mse_train = []
    mse_test = []

    # Run
    epochs = 10
    for e in range(epochs):

        # Shuffle training data
        shuffle_indices = np.random.permutation(np.arange(len(y_train)))
        X_train = X_train[shuffle_indices]
        y_train = y_train[shuffle_indices]

        # Minibatch training
        for i in range(0, len(y_train) // batch_size):
            start = i * batch_size
            batch_x = X_train[start:start + batch_size]
            batch_y = y_train[start:start + batch_size]
            # Run optimizer with batch
            net.run(opt, feed_dict={X: batch_x, Y: batch_y})

            # Show progress
            if np.mod(i, 50) == 0:
                # MSE train and test
                mse_train.append(net.run(mse, feed_dict={X: X_train, Y: y_train}))
                mse_test.append(net.run(mse, feed_dict={X: X_test, Y: y_test}))
                print('MSE Train: ', mse_train[-1])
                print('MSE Test: ', mse_test[-1])
                # Prediction
                pred = net.run(out, feed_dict={X: X_test})
                line2.set_ydata(pred)
                plt.title('Epoch ' + str(e) + ', Batch ' + str(i))
                plt.pause(0.01)
