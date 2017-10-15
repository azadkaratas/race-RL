from oyun import game_reset,game_loop
import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median

display_width = 200
display_height = 300

black = (33,33,33)
white = (255,255,255)
red = (255,0,0)

car_width = 25
car_height = 50
arac_hizi = 6
thing_width = 75
thing_height = 30
thing_speed = 3

target_score = 0.1
num_of_iteration = 20


training_data = []
accepted_scores = []
all_scores = []

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

    network = fully_connected(network, 3, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
    model = tflearn.DNN(network, tensorboard_dir='log')

    return model


model = neural_network_model(8)
model.load('ucuncuModelimiz.model')
game_reset()

for _ in range(num_of_iteration):
    
    #                   0           1             2           3       4 5     6         7        8     9
    #output = [thing_startx_old,thing_starty,thing_width,thing_height,x,y,car_width,car_height,score,done]

    game_memory = []
    done = 0
    score = 0

    #Önce boş bi hamle yapalım ki output datalardan konum bilgilerine ulaşabilelim.
    action = [0,0,0]
    output = game_loop(action)
        
    while not done:

        #We're making our move depending on the coming informations and model decides the output
        action = [0,0,0]
        X_woScaled = np.array(output[:-2]).reshape(-1,8,1)
        X = (X_woScaled +30)/(330)
        act = np.argmax(model.predict(X))            
        action[act] = 1
        print(model.predict(np.array(output[:-2]).reshape(-1,8,1)))
        output = game_loop(action)
            
        score += output[8]
        done = output[9]

        game_memory.append([output[:-2],action])

        if score >= target_score:
            accepted_scores.append(score)
    
        if done:
            game_reset()
            all_scores.append(score)
        

print('Average of all scores:',mean(all_scores))
print('Average of accepted score:',mean(accepted_scores))



