import pygame
import time
import random
import numpy as np

pygame.init()

display_width = 200
display_height = 300

black = (33,33,33)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('AI Racing')

clock = pygame.time.Clock()

car_width = 25
car_height = 50
car_speed = 5
thing_width = 75
thing_height = 30
thing_speed = 15  #This is the speed of falling block.

score_count = 0

def things(thingx,thingy,thingw,thingh,color):
    pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])
    
def car(x,y):
    things(x,y,car_width,car_height,red)
    
def calculateScore(car_x,thing_x):
    max_score = display_width - (car_width+thing_width)/2
    score = ((car_x + car_width/2) - (thing_x + thing_width/2)) / max_score
    score = np.abs(score)
    return score

def game_reset():
    global x,y,x_change,thing_starty,thing_startx,done
    x= random.randrange(0,display_width-car_width)
    y= (display_height * 0.8)
    done = 0
    x_change = 0
    thing_starty = -thing_height
    thing_startx = random.randrange(0,display_width-thing_width)
    
def game_loop(movement,quick_mode=0):    
    global x,y,x_change,thing_starty,thing_startx,done,score_count
    
    x_old = x
    ty_old = thing_starty    
    old_score = calculateScore(x_old,thing_startx)
    
    if movement == [1,0,0]:
        if x<car_speed:
            x_change = 0
        else:
            x_change = -car_speed
    elif movement == [0,1,0]:
        x_change = 0
    elif movement == [0,0,1]:
        if x> display_width - car_speed:
            x_change = 0
        else:
            x_change = car_speed

    x += x_change

    if not quick_mode:
        gameDisplay.fill(white)
        things(thing_startx,thing_starty,thing_width,thing_height,black)
    thing_starty += thing_speed
    thing_startx_old = thing_startx
    
    if not quick_mode:
        car(x,y)

    score = 0
    done = 0
    
    if x> display_width - car_width:
        x = display_width - car_width
    elif x<0:
        x = 0

    score = calculateScore(x,thing_startx_old)
    
    #####    YOU SCORED   ######                
    if thing_starty > display_height:
        thing_starty = 0 - thing_height
        thing_startx_old = thing_startx
        thing_startx = random.randrange(0,(display_width-thing_width))
        score_count = score_count+1
        done = 1
        if not quick_mode:
                print(score_count)
      
    #####    YOU CRASHED    ######   
    if y < thing_starty+thing_height:
        if x > thing_startx and x < thing_startx+thing_width or x+car_width > thing_startx and x+car_width<thing_startx+thing_width:
            score_count = 0
            if not quick_mode:
                print('You Crashed!')
                print(score_count)
            done = 1

    danger = 0
    ####  CHECKING THE DANGER SITUATIONS   ####
    if x > thing_startx and x < thing_startx+thing_width or x+car_width > thing_startx and x+car_width < thing_startx+thing_width:
            danger = 1

            
    ### HERE IS SENDING OUTPUTS after normalization process  ###
    output = [thing_startx / display_width,ty_old / display_height,x_old / display_width,score-old_score,danger,done]
    #print(output)
    if not quick_mode:
        pygame.display.update()
        clock.tick(60)

    return output
