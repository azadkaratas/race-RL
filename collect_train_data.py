from race_game import game_reset,game_loop
import random
import numpy as np
from statistics import mean

num_of_iteration = 50000

training_data = []
accepted_scores = []

quick_collect = 1 # To collect data without watching the, set this value as 1.
game_reset()

for i in range(num_of_iteration):
    
    #            0           1       2          3          4     5 
    #output = [thing_startx,ty_old,x_old,score-old_score,danger,done]
    
    done = 0
    score = 0

    #We're making our random move and hold the output if it satisfy the score and danger criteria
    action = [0,0,0]
    action[random.randrange(3)] = 1
    output = game_loop(action,quick_collect)
    
    score = output[3]
    danger = output[4]
    
    done = output[5]

    if score >= 0.01:
        training_data.append([output[:3],action])
        accepted_scores.append(score)
    elif score > 0 and score < 0.01:
        if danger == 0:
            training_data.append([output[:3],action])
            accepted_scores.append(score)
    
    if done:
        game_reset()
        

training_data_save = np.array(training_data)
np.save('saved.npy',training_data_save)

print('Training data saved.')
print('Average of accepted score:',mean(accepted_scores))
print('Size of accepted score:',np.size(accepted_scores))



