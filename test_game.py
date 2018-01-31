from race_game import game_reset,game_loop
import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

num_of_iteration=100
LR = 1e-3

def neural_network_model(input_size):

    network = input_data(shape=[None, input_size, 1], name='input')

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, input_size, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
    model = tflearn.DNN(network, tensorboard_dir='log')

    return model

input_size = 3
model = neural_network_model(input_size)
model.load('firstModel.model')

game_reset()

for _ in range(num_of_iteration):
    
    #               0          1       2        3              4     5 
    #output = [thing_startx, ty_old, x_old, score-old_score,danger,done]
    
    #First movement is random to get output data of initial frame.
    action = [0,0,0]
    output = game_loop(action)
        
    done = 0
    
    while not done:
        #We're making our move depending on the coming informations and model decides the output
        action = [0,0,0]
        X  = np.array(output[:3]).reshape(-1,3,1)
        #print(X)
        action = [0,0,0]
        act = np.argmax(model.predict(X))            
        action[act] = 1

        #print(action)
        output = game_loop(action)
        done = output[5]
        
        if done:
            game_reset() 
        
