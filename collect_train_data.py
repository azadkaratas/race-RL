from oyun import game_reset,game_loop
import random
import numpy as np
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

target_score = 0.5
num_of_iteration = 15000


training_data = []
accepted_scores = []
all_scores = []

game_reset()

for _ in range(num_of_iteration):
    
    #                   0           1             2           3       4 5     6         7        8     9
    #output = [thing_startx_old,thing_starty,thing_width,thing_height,x,y,car_width,car_height,score,done]

    game_memory = []
    done = 0
    score = 0
    while not done:

        #We're making our random move and hold the output
        action = [0,0,0]
        action[random.randrange(3)] = 1
        output = game_loop(action)
        
        score += output[8]
        done = output[9]

        game_memory.append([output[:-2],action])

        if score >= target_score:
            accepted_scores.append(score)

            for data in game_memory:
                training_data.append([data[0],data[1]])
    
        if done:
            game_reset()
            all_scores.append(score)
        

training_data_save = np.array(training_data)
np.save('saved2.npy',training_data_save)

print('Average of all scores:',mean(all_scores))
print('Average of accepted score:',mean(accepted_scores))



