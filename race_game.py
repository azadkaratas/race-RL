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
pygame.display.set_caption('Learning Racing')

saat = pygame.time.Clock()

car_width = 25
car_height = 50
car_speed = 6
thing_width = 75
thing_height = 30
thing_speed = 3

def things(thingx,thingy,thingw,thingh,color):
    pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])
    
def car(x,y):
    things(x,y,car_width,car_height,red)
    
def youScored(car_x,thing_x):
    max_score = display_width - (car_width+thing_width)/2
    score = ((car_x + car_width/2) - (thing_x + thing_width/2)) / max_score
    score = np.abs(score)
    print('Score is:',score)
    return score

def game_reset():
    global x,y,x_change,thing_starty,thing_startx,done
    x= (display_width * 0.45)
    y= (display_height * 0.8)

    done = 0
    x_change = 0

    thing_starty = -thing_height
    thing_startx = random.randrange(0,display_width-thing_width)

    
def game_loop(movement):    
    global x,y,x_change,thing_starty,thing_startx,done

    if movement == [1,0,0]:
        if x<=0:
            x_change = 0
        else:
            x_change = -car_speed
    elif movement == [0,1,0]:
        x_change = 0
    elif movement == [0,0,1]:
        if x>= display_width - car_width:
            x_change = 0
        else:
            x_change = car_speed

    x += x_change
    
    gameDisplay.fill(white)
    things(thing_startx,thing_starty,thing_width,thing_height,black)
    thing_starty += thing_speed
    thing_startx_old = thing_startx
    
    car(x,y)

    score = 0
    done = 0
    
    if x> display_width - car_width:
        x = display_width - car_width
    elif x<0:
        x = 0

    #####    YOU SCORED   ######                
    if thing_starty > display_height:
        thing_starty = 0 - thing_height
        thing_startx_old = thing_startx
        thing_startx = random.randrange(0,(display_width-thing_width))
        score = youScored(x,thing_startx_old)
        done = 1
      
    #####    YOU CRASHED    ######   
    if y < thing_starty+thing_height:
        if x > thing_startx and x < thing_startx+thing_width or x+car_width > thing_startx and x+car_width<thing_startx+thing_width:
            print('You Crashed!')
            done = 1

            
    # HERE IS SENDING OUTPUTS
    output = [thing_startx_old,thing_starty,thing_width,thing_height,x,y,car_width,car_height,score,done]
    #print(output)
    pygame.display.update()
    saat.tick(60)

    return output
