# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 21:00:43 2021

@author: wasil
"""

# Import the pygame library and initialise the game engine
import pygame
from pygame.locals import *
import random
import pickle

pygame.init()

# to diplay the text
font = pygame.font.Font(pygame.font.get_default_font(), 36)
font2 = pygame.font.Font(pygame.font.get_default_font(), 18)

IMAGE = pygame.image.load('car4.png')
IMAGE = pygame.transform.scale(IMAGE, (60, 60))

PASSENGER = pygame.image.load('passenger.png')
PASSENGER = pygame.transform.scale(PASSENGER, (60, 60))

DROPOFF = pygame.image.load('loca.png')
DROPOFF = pygame.transform.scale(DROPOFF, (60, 60))

GRAY = (192, 192, 192)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230	)

DARK_GRAY = (88,88,88)
LIGHT_GRAY = (169,169,169)

# spaces around the board
SPACING = 20
# spaces between the lines
LINE_SPACING = 92
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Open a new window
size = (500, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Smart Cab")


PASSENGER_POS = [[0, 0], [4, 0], [0, 4], [4, 3]]

PASSENGER_PICKED = False
PASSENGER_DROPPED = False

pickup_position = 0
dropoff_position = 0

REWARD = 0
NEW_GAME = False
ACTION = None
CUMULATIVE_REWARD = 0
CUMULATIVE_REWARD_LIST = []
# COUNTER TO SAVE CUMULATIVE_REWARD_LIST
C = 0
C_limit = 10_000

def GameBoard(I=None, J=None):
    
    # Display the Actions / coordinates.
    # x=0, y=500, w=500, h=200
    action_rect = Rect(0, 500, 500, 200)
    # Lower rectangle.
    pygame.draw.rect(screen, GRAY, action_rect)
    
    # The main screen
    # For game screen
    # x=0, y=0, w=500, h=500
    game_rect = Rect(0, 0, 500, 500)
    # uppper rectangle.
    pygame.draw.rect(screen, DARK_GRAY, game_rect)
    
    # The Game Board
    # For game screen
    # x=0, y=0, w=500, h=500
    game_rect = Rect(SPACING, SPACING, 500-(SPACING*2), 500-(SPACING*2))
    # game rectangle.
    pygame.draw.rect(screen, LIGHT_GRAY, game_rect)
    
    # RED BOUNDARY
    pygame.draw.rect(screen, RED, game_rect, 3)
    
    # drop off and pick up location.
    # with color light blue
    x_imd_point = (LINE_SPACING*(1-1))+20  + ((LINE_SPACING*1)+20 - (LINE_SPACING*(1-1))+20 )/2
    y_imd_point = (LINE_SPACING*(5-1))+20  + ((LINE_SPACING*5)+20 - (LINE_SPACING*(5-1))+20 )/2
    pygame.draw.rect(screen, LIGHT_BLUE, (x_imd_point-65, y_imd_point-65, 90, 90) )
    
    x_imd_point = (LINE_SPACING*(1-1))+20  + ((LINE_SPACING*1)+20 - (LINE_SPACING*(1-1))+20 )/2
    y_imd_point = (LINE_SPACING*(1-1))+20  + ((LINE_SPACING*1)+20 - (LINE_SPACING*(1-1))+20 )/2
    pygame.draw.rect(screen, LIGHT_BLUE, (x_imd_point-65, y_imd_point-65, 90, 90) )
    
    x_imd_point = (LINE_SPACING*(5-1))+20  + ((LINE_SPACING*5)+20 - (LINE_SPACING*(5-1))+20 )/2
    y_imd_point = (LINE_SPACING*(1-1))+20  + ((LINE_SPACING*1)+20 - (LINE_SPACING*(1-1))+20 )/2
    pygame.draw.rect(screen, LIGHT_BLUE, (x_imd_point-65, y_imd_point-65, 90, 90) )
    
    x_imd_point = (LINE_SPACING*(4-1))+20  + ((LINE_SPACING*4)+20 - (LINE_SPACING*(4-1))+20 )/2
    y_imd_point = (LINE_SPACING*(5-1))+20  + ((LINE_SPACING*5)+20 - (LINE_SPACING*(5-1))+20 )/2
    pygame.draw.rect(screen, LIGHT_BLUE, (x_imd_point-65, y_imd_point-65, 90, 90) )
    
    # lines
    for i in range(1,5):
        pygame.draw.line(screen, WHITE, ((LINE_SPACING*i)+20, 20), ( (LINE_SPACING*i)+20, 480), 3)
        pygame.draw.line(screen, WHITE, (20, (LINE_SPACING*i)+20), ( 480, (LINE_SPACING*i)+20), 3)
        
    # create Walls
    pygame.draw.line(screen, RED, ((LINE_SPACING*1)+20, 296), ( (LINE_SPACING*1)+20, 480), 10)
    pygame.draw.line(screen, RED, ((LINE_SPACING*3)+20, 296), ( (LINE_SPACING*3)+20, 480), 10)
    
    pygame.draw.line(screen, RED, ((LINE_SPACING*2)+20, 20), ( (LINE_SPACING*2)+20, (LINE_SPACING*1)+20), 10)
    
    if(I != None and J != None):
        x, y = coordinate(I, J)
        screen.blit(IMAGE, (x-30, y-30) )
    

def states(x, y):
    """
    Input states. Output coordinates.
    """
    # i here represent column
    for i in range(1, 6):
        #if(x > (i*20) and x < (LINE_SPACING*i)+20):
        firstline_vertical = (LINE_SPACING*(i-1))+20
        secondline_vertical = (LINE_SPACING*i)+20
        if(x >  firstline_vertical and x < secondline_vertical):
            # j here represent row
            for j in range(1, 6):
                firstline_horizontal = (LINE_SPACING*(j-1))+20
                secondline_horizontal = (LINE_SPACING*j)+20
                if (y > firstline_horizontal and y < secondline_horizontal):
                    return j-1, i-1
                    

def coordinate(I, J):
    """
    Input coordinates. Output states.
    """
    cumulative_linespacing_Y = 0
    cumulative_linespacing_X = 0
    for i in range(1, 6):        
        cumulative_linespacing_Y += LINE_SPACING
        if (i-1 == I):            
            
            # here, 26 is hardoded number
            # Changes the position Left or Right.
            y = (cumulative_linespacing_Y)-26#+(LINE_SPACING*(i-1))            
            for j in range(1, 6):
                cumulative_linespacing_X += LINE_SPACING
                if (j-1 == J):
                    x = (cumulative_linespacing_X)-26#+(LINE_SPACING*(i-1))       
                    return x, y
        
def rot_center(image, angle):
    
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image    

def cell_position_key(action, x, y):
    if action == "RIGHT":
        x = x+92        
        rot_image = rot_center(IMAGE, -90)
        screen.blit(rot_image, (x-30, y-30))
    if action == "LEFT":
        x = x-92        
        rot_image = rot_center(IMAGE, 90)
        screen.blit(rot_image, (x-30, y-30))
    if action == "UP":
        y = y-92        
        screen.blit(IMAGE, (x-30, y-30))
    if action == "DOWN":
        y = y+92        
        rot_image = rot_center(IMAGE, 180)
        screen.blit(rot_image, (x-30, y-30))
        
    return int(x), int(y)

def passenger_update(pickup_position):
    global PASSENGER_PICKED
    
    if(PASSENGER_PICKED == False):
        # get the passenger states
        passenger_states = PASSENGER_POS[pickup_position]    
        # display the sprite
        passenger_sprite(passenger_states)

def dropoff_update(dropoff_position):
    global PASSENGER_DROPPED
    
    if PASSENGER_DROPPED == False:
        # dropoff location
        dropoff_states = PASSENGER_POS[dropoff_position]    
        # display the sprite
        dropoff_sprite(dropoff_states)

def passenger_sprite(passenger_states):
    """
    To display the passenger sprite
    """
    # converts states into coordinates
    x, y = coordinate(passenger_states[0], passenger_states[1])
    screen.blit(PASSENGER, ((x-30, y-30)))
    
def dropoff_sprite(dropoff_states):
    """
    To display the dropoff sprite
    """    
    # converts states into coordinates
    x, y = coordinate(dropoff_states[0], dropoff_states[1])
    screen.blit(DROPOFF, ((x-30, y-30)))

def game_logic(I, J, p_I, p_J, pickup_position, dropoff_position):
   
    global PASSENGER_PICKED
    global PASSENGER_DROPPED
    
    global REWARD
    
    global ACTION
    global CUMULATIVE_REWARD
        
    # dropoff location, I and J
    d_I = PASSENGER_POS[dropoff_position][0]    
    d_J = PASSENGER_POS[dropoff_position][1]
    
    # and then update the text
    text_surface = font2.render(f'Drop off location - {d_I}{d_J}'.format(d_I, d_J), False, (255, 255, 255))
    screen.blit(text_surface, dest=(150,625))
    
    # if we havent pick up the passenger yet
    if PASSENGER_PICKED == False:
        
        # at every step
        REWARD = -1
        
        # if the cab tries to pick the passenger from wrong location.
        wrong_pick_up = [i for i in [0, 1, 2, 3] if i != pickup_position]
        
        if ( (PASSENGER_POS[wrong_pick_up[0]][0] == I) and (PASSENGER_POS[wrong_pick_up[0]][1] == J)):
            REWARD = -10
        elif ( (PASSENGER_POS[wrong_pick_up[1]][0] == I) and (PASSENGER_POS[wrong_pick_up[1]][1] == J)):
            REWARD = -10
        elif ( (PASSENGER_POS[wrong_pick_up[2]][0] == I) and (PASSENGER_POS[wrong_pick_up[2]][1] == J)):
            REWARD = -10
        # first check the car and the passenger positions
        elif( I == p_I and J == p_J):
            p_I = I
            p_J = J
            REWARD = 30
            PASSENGER_PICKED = True
            # now the passenger location is same as car's location
            
        return p_I, p_J, REWARD, PASSENGER_PICKED
            
    
    # if the pssenger is picked, then the passenger's location is same as cab's location.
    if(PASSENGER_PICKED == True):
        # the cab's location is now same as passenger's location.
        p_I = I
        p_J = J
        # if the cab tries to DROP OFF the passenger TO wrong location.
        wrong_drop_off = [i for i in [0, 1, 2, 3] if (i != dropoff_position)  ]  # and (i != pickup_position)
        
        if ( (PASSENGER_POS[wrong_drop_off[0]][0] == I) and (PASSENGER_POS[wrong_drop_off[0]][1] == J)):
            REWARD = -10
        elif ( (PASSENGER_POS[wrong_drop_off[1]][0] == I) and (PASSENGER_POS[wrong_drop_off[1]][1] == J)):
            REWARD = -10
        elif ( (PASSENGER_POS[wrong_drop_off[2]][0] == I) and (PASSENGER_POS[wrong_drop_off[2]][1] == J)):
            REWARD = -10
        else:
            
            REWARD = -1
        return p_I, p_J, REWARD, PASSENGER_PICKED
       
def restart(I, J, p_I, p_J):
    
    global PASSENGER_PICKED
    global PASSENGER_DROPPED
    
    global pickup_position
    global dropoff_position
    
    global NEW_GAME
    # pickup location of the passenger, a new location   
    pickup_position = random.randint(0, 3)
    
    # new p_I and p_J
    p_I = PASSENGER_POS[pickup_position][0]    
    p_J = PASSENGER_POS[pickup_position][1]
    
    # dropoff position shuuld be different from pickoff location
    dropoff_position = k = random.choice([i for i in [0, 1, 2, 3] if i != pickup_position])
    
    PASSENGER_PICKED = False
    NEW_GAME = False
    
    passenger_update(pickup_position)
    dropoff_update(dropoff_position)
    
    # again check th game logic, 
    # becoz there might
    p_I, p_J, REWARD, PASSENGER_PICKED = game_logic(I, J, p_I, p_J, pickup_position, dropoff_position)
    
    return NEW_GAME, p_I, p_J, REWARD, PASSENGER_PICKED
    

def mainGame(get_actions, counter, run, input_):
    global pickup_position
    global dropoff_position
    
    global PASSENGER_PICKED
    
    global ACTION
    
    global CUMULATIVE_REWARD
    global REWARD
    
    global NEW_GAME
    global CUMULATIVE_REWARD_LIST, C
    
    GameBoard()
    
    # place the car
    # To find the mid point
    initial_x = 2
    initial_y = 5
    
    x = x_imd_point = ((LINE_SPACING*(initial_x-1))+20)  + (((LINE_SPACING*initial_x)+20) - ((LINE_SPACING*(initial_x-1))+20) )/2
    y = y_imd_point = ((LINE_SPACING*(initial_y-1))+20)  + (((LINE_SPACING*initial_y)+20) - ((LINE_SPACING*(initial_y-1))+20) )/2
    screen.blit(IMAGE,   (x_imd_point-30, y_imd_point-30))
    
    I, J = states(x, y)

    # pickup location of the passenger    
    pickup_position = random.randint(0, 3)
    
    # dropoff position shuuld be different from pickoff location
    dropoff_position = k = random.choice([i for i in [0, 1, 2, 3] if i != pickup_position])
    
    passenger_update(pickup_position)
    dropoff_update(dropoff_position)
    
    p_I = PASSENGER_POS[pickup_position][0]
    p_J = PASSENGER_POS[pickup_position][1]

    # to display the States            
    # lower rectangle.
    
    # --- Go ahead and update the screen with what we've drawn.
    text_surface = font.render(f'State: {I}, {J}'.format(I, J), False, (255, 255, 255))
    screen.blit(text_surface, dest=(150,550))
    
    # update cab's location
    text_surface = font2.render(f'Passenger location - {p_I}{p_J}'.format(p_I, p_J), False, (255, 255, 255))
    screen.blit(text_surface, dest=(150,600))
    
    # and then update the text
    d_I = PASSENGER_POS[dropoff_position][0]
    d_J = PASSENGER_POS[dropoff_position][1]
    text_surface = font2.render(f'Drop off location - {d_I}{d_J}'.format(d_I, d_J), False, (255, 255, 255))
    screen.blit(text_surface, dest=(150,625))
    
    # random initial policy
    ACTION = "UP"
    
    # -------- Main Program Loop -----------
    game = True
    while game:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                game = False # Flag that we are done so we exit this loop
            """
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RIGHT:
                    if (J < 4):
                        if ( (I != 3 or J != 2) and (I != 4 or J != 2) and (I != 3 or J != 0) and (I != 4 or J != 0) and (I != 0 or J != 1) ):
                            
                            GameBoard()                

                            x, y = cell_position_key("RIGHT", x, y)
                            I, J = states(x, y)
                            # check of we dropped the passenger or not.
                            p_I, p_J, REWARD, PASSENGER_PICKED = game_logic(I, J, p_I, p_J, pickup_position, dropoff_position)
                            
                            # only drop off when you are at drop off location and already picked up the passenger.
                            if((I == PASSENGER_POS[dropoff_position][0] and J == PASSENGER_POS[dropoff_position][1]) and (PASSENGER_PICKED == True)):
                                REWARD = 20
                                NEW_GAME = True

                            print(REWARD)
                            CUMULATIVE_REWARD += REWARD
                            #ACTION = 
                            #get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                            #ACTION = run(I, J, p_I, p_J, dropoff_position)
                            # display reward
                            #print("the cumulative reward is: ", CUMULATIVE_REWARD)
                            text_surface = font2.render(f'Reward-> {REWARD}'.format(REWARD), False, (255, 255, 255))
                            screen.blit(text_surface, dest=(150,650))
                            
                            if(NEW_GAME == True):
                                print("the cumulative reward is: ", CUMULATIVE_REWARD)
                                counter(input_)
                                # first remove the previous dropped location
                                # cumulation of rewards at each episode.
                                CUMULATIVE_REWARD = 0
                                GameBoard(I, J)     
                                NEW_GAME, p_I, p_J, REWARD, PASSENGER_PICKED = restart(I, J, p_I, p_J)
                            # update cab's location
                            text_surface = font2.render(f'Passenger location - {p_I}{p_J}'.format(p_I, p_J), False, (255, 255, 255))
                            screen.blit(text_surface, dest=(150,600))
                        else:
                            REWARD = -1                            
                    else:
                        REWARD = -1
                if event.key == pygame.K_LEFT:
                    if (J > 0):
                        if ( (I != 4 or J != 1) and (I != 3 or J != 1) and  (I != 3 or J != 3) and (I != 4 or J != 3) and  (I != 0 or J != 2)  ):
                            
                            GameBoard()                    
                            
                            
                            x, y = cell_position_key("LEFT", x, y)
                            #print("Coordinate:", x, y)
                            I, J = states(x, y)
                            # check of we dropped the passenger or not.
                            p_I, p_J, REWARD, PASSENGER_PICKED = game_logic(I, J, p_I, p_J, pickup_position, dropoff_position)
                            
                            # only drop off when you are at drop off location and already picked up the passenger.
                            if((I == PASSENGER_POS[dropoff_position][0] and J == PASSENGER_POS[dropoff_position][1]) and (PASSENGER_PICKED == True)):
                                REWARD = 20
                                NEW_GAME = True
                        
                        
                            print(REWARD)
                            CUMULATIVE_REWARD += REWARD
                            #ACTION = 
                            #get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                            #ACTION = run(I, J, p_I, p_J, dropoff_position)
                            # display reward
                            #print("the cumulative reward is: ", CUMULATIVE_REWARD)
                            text_surface = font2.render(f'Reward-> {REWARD}'.format(REWARD), False, (255, 255, 255))
                            screen.blit(text_surface, dest=(150,650))
                            
                            if(NEW_GAME == True):
                                print("the cumulative reward is: ", CUMULATIVE_REWARD)
                                counter(input_)
                                # first remove the previous dropped location
                                # cumulation of rewards at each episode.
                                CUMULATIVE_REWARD = 0
                                GameBoard(I, J)
                                NEW_GAME, p_I, p_J, REWARD, PASSENGER_PICKED = restart(I, J, p_I, p_J)
                            # update cab's location
                            text_surface = font2.render(f'Passenger location - {p_I}{p_J}'.format(p_I, p_J), False, (255, 255, 255))
                            screen.blit(text_surface, dest=(150,600))
                    
                        else:
                            REWARD = -1                               
                    else:
                        REWARD = -1
                
                if event.key == pygame.K_UP:
                    if (I > 0):
                        GameBoard()
                        
                        
                        x, y = cell_position_key("UP", x, y)
                        I, J = states(x, y)
                        # check of we dropped the passenger or not.
                        p_I, p_J, REWARD, PASSENGER_PICKED = game_logic(I, J, p_I, p_J, pickup_position, dropoff_position)
                        
                        # only drop off when you are at drop off location and already picked up the passenger.
                        if((I == PASSENGER_POS[dropoff_position][0] and J == PASSENGER_POS[dropoff_position][1]) and (PASSENGER_PICKED == True)):
                            REWARD = 20
                            NEW_GAME = True
                    
                    
                        print(REWARD)
                        CUMULATIVE_REWARD += REWARD
                        #ACTION = 
                        #get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                        #ACTION = run(I, J, p_I, p_J, dropoff_position)
                        # display reward
                        #print("the cumulative reward is: ", CUMULATIVE_REWARD)
                        text_surface = font2.render(f'Reward-> {REWARD}'.format(REWARD), False, (255, 255, 255))
                        screen.blit(text_surface, dest=(150,650))
                        
                        if(NEW_GAME == True):
                            print("the cumulative reward is: ", CUMULATIVE_REWARD)
                            counter(input_)
                            # first remove the previous dropped location
                            # cumulation of rewards at each episode.
                            CUMULATIVE_REWARD = 0
                            GameBoard(I, J)
                            NEW_GAME, p_I, p_J, REWARD, PASSENGER_PICKED = restart(I, J, p_I, p_J)
                        # update cab's location
                        text_surface = font2.render(f'Passenger location - {p_I}{p_J}'.format(p_I, p_J), False, (255, 255, 255))
                        screen.blit(text_surface, dest=(150,600))
                    else:
                        REWARD = -1
                if event.key == pygame.K_DOWN:
                    if(I < 4):
                    
                        GameBoard()
                        
                        x, y = cell_position_key("DOWN", x, y)
                        I, J = states(x, y)
                        # check of we dropped the passenger or not.
                        p_I, p_J, REWARD, PASSENGER_PICKED = game_logic(I, J, p_I, p_J, pickup_position, dropoff_position)
                            
                        # only drop off when you are at drop off location and already picked up the passenger.
                        if((I == PASSENGER_POS[dropoff_position][0] and J == PASSENGER_POS[dropoff_position][1]) and (PASSENGER_PICKED == True)):
                            REWARD = 20
                            NEW_GAME = True
                    
                    
                        print(REWARD)
                        CUMULATIVE_REWARD += REWARD
                        #ACTION = 
                        #get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                        #ACTION = run(I, J, p_I, p_J, dropoff_position)
                        # display reward
                        #print("the cumulative reward is: ", CUMULATIVE_REWARD)
                        text_surface = font2.render(f'Reward-> {REWARD}'.format(REWARD), False, (255, 255, 255))
                        screen.blit(text_surface, dest=(150,650))
                        
                        if(NEW_GAME == True):
                            print("the cumulative reward is: ", CUMULATIVE_REWARD)
                            counter(input_)
                            # first remove the previous dropped location
                            # cumulation of rewards at each episode.
                            CUMULATIVE_REWARD = 0
                            GameBoard(I, J)
                            NEW_GAME, p_I, p_J, REWARD, PASSENGER_PICKED = restart(I, J, p_I, p_J)
                            
                        # update cab's location
                        text_surface = font2.render(f'Passenger location - {p_I}{p_J}'.format(p_I, p_J), False, (255, 255, 255))
                        screen.blit(text_surface, dest=(150,600))
                    else:
                        REWARD = -1
        
        """
        # from RL task
        if ACTION == "RIGHT":
            if (J < 4):
                if ( (I != 3 or J != 2) and (I != 4 or J != 2) and (I != 3 or J != 0) and (I != 4 or J != 0) and (I != 0 or J != 1) ):
                    
                    GameBoard()                

                    x, y = cell_position_key("RIGHT", x, y)

                    I, J = states(x, y)
                    # check If we dropped the passenger or not.
                    p_I, p_J, REWARD, PASSENGER_PICKED = game_logic(I, J, p_I, p_J, pickup_position, dropoff_position)
                    
                    # only drop off when you are at drop off location and already picked up the passenger.
                    if((I == PASSENGER_POS[dropoff_position][0] and J == PASSENGER_POS[dropoff_position][1]) and (PASSENGER_PICKED == True)):
                        REWARD = 20
                        NEW_GAME = True

                    CUMULATIVE_REWARD += REWARD
                    if input_ == "TRAIN":
                        ACTION = get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                    elif input_ == "RUN":
                        ACTION = run(I, J, p_I, p_J, dropoff_position)
                    
                    # display reward

                    text_surface = font2.render(f'Reward-> {REWARD}'.format(REWARD), False, (255, 255, 255))
                    screen.blit(text_surface, dest=(150,670))
                    
                    if(NEW_GAME == True):
                        
                        CUMULATIVE_REWARD_LIST.append(CUMULATIVE_REWARD)
                        C+=1
                        if C % C_limit == 0:
                            with open(f"cumulative_reward_{C}.txt".format(C), "wb") as fp:   #Pickling
                                pickle.dump(CUMULATIVE_REWARD_LIST, fp)
                            
                                CUMULATIVE_REWARD_LIST=[]
                        print("the cumulative reward is: ", CUMULATIVE_REWARD)
                        
                        counter(input_)
                        # first remove the previous dropped location
                        # cumulation of rewards at each episode.
                        CUMULATIVE_REWARD = 0
                        GameBoard(I, J)
                        NEW_GAME, p_I, p_J, REWARD, PASSENGER_PICKED = restart(I, J, p_I, p_J)
                    # update cab's location
                    text_surface = font2.render(f'Passenger location - {p_I}{p_J}'.format(p_I, p_J), False, (255, 255, 255))
                    screen.blit(text_surface, dest=(150,600))
                else:
                    REWARD = -1
                    if input_ == "TRAIN":
                        ACTION = get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                    elif input_ == "RUN":
                        ACTION = run(I, J, p_I, p_J, dropoff_position)
            else:
                    REWARD = -1
                    if input_ == "TRAIN":
                        ACTION = get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                    elif input_ == "RUN":
                        ACTION = run(I, J, p_I, p_J, dropoff_position)
        
        if ACTION == "LEFT":
            if (J > 0):
                if ( (I != 4 or J != 1) and (I != 3 or J != 1) and  (I != 3 or J != 3) and (I != 4 or J != 3) and  (I != 0 or J != 2)  ):
                    
                    GameBoard()                

                    x, y = cell_position_key("LEFT", x, y)

                    I, J = states(x, y)
                    # check of we dropped the passenger or not.
                    p_I, p_J, REWARD, PASSENGER_PICKED = game_logic(I, J, p_I, p_J, pickup_position, dropoff_position)
                    
                    # only drop off when you are at drop off location and already picked up the passenger.
                    if((I == PASSENGER_POS[dropoff_position][0] and J == PASSENGER_POS[dropoff_position][1]) and (PASSENGER_PICKED == True)):
                        REWARD = 20
                        NEW_GAME = True
                
                    CUMULATIVE_REWARD += REWARD
                    if input_ == "TRAIN":
                        ACTION = get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                    elif input_ == "RUN":
                        ACTION = run(I, J, p_I, p_J, dropoff_position)
                    # display reward

                    text_surface = font2.render(f'Reward-> {REWARD}'.format(REWARD), False, (255, 255, 255))
                    screen.blit(text_surface, dest=(150,670))
                    
                    if(NEW_GAME == True):
                        CUMULATIVE_REWARD_LIST.append(CUMULATIVE_REWARD)
                        C+=1
                        if C % C_limit == 0:
                            with open(f"cumulative_reward_{C}.txt".format(C), "wb") as fp:   #Pickling
                                pickle.dump(CUMULATIVE_REWARD_LIST, fp)
                            
                                CUMULATIVE_REWARD_LIST=[]
                        print("the cumulative reward is: ", CUMULATIVE_REWARD)
                        counter(input_)
                        # first remove the previous dropped location
                        # cumulation of rewards at each episode.
                        CUMULATIVE_REWARD = 0
                        GameBoard(I, J)
                        NEW_GAME, p_I, p_J, REWARD, PASSENGER_PICKED = restart(I, J, p_I, p_J)
                    # update cab's location
                    text_surface = font2.render(f'Passenger location - {p_I}{p_J}'.format(p_I, p_J), False, (255, 255, 255))
                    screen.blit(text_surface, dest=(150,600))
                else:
                    REWARD = -1
                    if input_ == "TRAIN":
                        ACTION = get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                    elif input_ == "RUN":
                        ACTION = run(I, J, p_I, p_J, dropoff_position)
            else:
                    REWARD = -1
                    if input_ == "TRAIN":
                        ACTION = get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                    elif input_ == "RUN":
                        ACTION = run(I, J, p_I, p_J, dropoff_position)

        if ACTION == "UP":
            if (I > 0):
            
                GameBoard()                

                x, y = cell_position_key("UP", x, y)
                
                I, J = states(x, y)
                # check of we dropped the passenger or not.
                p_I, p_J, REWARD, PASSENGER_PICKED = game_logic(I, J, p_I, p_J, pickup_position, dropoff_position)
                
                # only drop off when you are at drop off location and already picked up the passenger.
                if((I == PASSENGER_POS[dropoff_position][0] and J == PASSENGER_POS[dropoff_position][1]) and (PASSENGER_PICKED == True)):
                    REWARD = 20
                    NEW_GAME = True

                CUMULATIVE_REWARD += REWARD
                if input_ == "TRAIN":
                    ACTION = get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                elif input_ == "RUN":
                    ACTION = run(I, J, p_I, p_J, dropoff_position)
                # display reward
                
                text_surface = font2.render(f'Reward-> {REWARD}'.format(REWARD), False, (255, 255, 255))
                screen.blit(text_surface, dest=(150,670))
                
                if(NEW_GAME == True):
                    CUMULATIVE_REWARD_LIST.append(CUMULATIVE_REWARD)
                    C+=1
                    if C % C_limit == 0:
                        with open(f"cumulative_reward_{C}.txt".format(C), "wb") as fp:   #Pickling
                            pickle.dump(CUMULATIVE_REWARD_LIST, fp)
                        
                            CUMULATIVE_REWARD_LIST=[]
                    print("the cumulative reward is: ", CUMULATIVE_REWARD)
                    
                    counter(input_)
                    # first remove the previous dropped location
                    # cumulation of rewards at each episode.
                    CUMULATIVE_REWARD = 0
                    GameBoard(I, J)
                    NEW_GAME, p_I, p_J, REWARD, PASSENGER_PICKED = restart(I, J, p_I, p_J)
                # update cab's location
                text_surface = font2.render(f'Passenger location - {p_I}{p_J}'.format(p_I, p_J), False, (255, 255, 255))
                screen.blit(text_surface, dest=(150,600))
            else:
                REWARD = -1
                if input_ == "TRAIN":
                    ACTION = get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                elif input_ == "RUN":
                    ACTION = run(I, J, p_I, p_J, dropoff_position)
            

        if ACTION == "DOWN":
            if(I < 4):
            
                GameBoard()                

                x, y = cell_position_key("DOWN", x, y)
                
                I, J = states(x, y)
                # check of we dropped the passenger or not.
                p_I, p_J, REWARD, PASSENGER_PICKED = game_logic(I, J, p_I, p_J, pickup_position, dropoff_position)
                
                # only drop off when you are at drop off location and already picked up the passenger.
                if((I == PASSENGER_POS[dropoff_position][0] and J == PASSENGER_POS[dropoff_position][1]) and (PASSENGER_PICKED == True)):
                    REWARD = 20
                    NEW_GAME = True
                    
                CUMULATIVE_REWARD += REWARD
                if input_ == "TRAIN":
                    ACTION = get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                elif input_ == "RUN":
                    ACTION = run(I, J, p_I, p_J, dropoff_position)
                    
                # display reward

                text_surface = font2.render(f'Reward-> {REWARD}'.format(REWARD), False, (255, 255, 255))
                screen.blit(text_surface, dest=(150,670))
                
                if(NEW_GAME == True):
                    CUMULATIVE_REWARD_LIST.append(CUMULATIVE_REWARD)
                    
                    C+=1
                    if C % C_limit == 0:
                        with open(f"cumulative_reward_{C}.txt".format(C), "wb") as fp:   #Pickling
                            pickle.dump(CUMULATIVE_REWARD_LIST, fp)
                        
                            CUMULATIVE_REWARD_LIST=[]
                    print("the cumulative reward is: ", CUMULATIVE_REWARD)

                    counter(input_)
                    # first remove the previous dropped location
                    # cumulation of rewards at each episode.
                    CUMULATIVE_REWARD = 0
                    GameBoard(I, J)
                    NEW_GAME, p_I, p_J, REWARD, PASSENGER_PICKED = restart(I, J, p_I, p_J)
                # update cab's location
                text_surface = font2.render(f'Passenger location - {p_I}{p_J}'.format(p_I, p_J), False, (255, 255, 255))
                screen.blit(text_surface, dest=(150,600))
            else:
                REWARD = -1
                if input_ == "TRAIN":
                    ACTION = get_actions(I, J, p_I, p_J, dropoff_position, REWARD)
                elif input_ == "RUN":
                    ACTION = run(I, J, p_I, p_J, dropoff_position)
        # pick from here
        passenger_update(pickup_position)        
        # drop here
        dropoff_update(dropoff_position)
        # to display the States            
        # lower rectangle.
        # --- Go ahead and update the screen with what we've drawn.
        text_surface = font.render(f'State: {I}, {J}'.format(I, J), False, (255, 255, 255))
        screen.blit(text_surface, dest=(150,550))
        
        # --- Limit to 60 frames per second
        if input_ == "TRAIN":
            clock.tick(0)
            #pygame.display.update()
        elif input_ == "RUN":
            clock.tick(10)
            pygame.display.update()
     
    #Once we have exited the main program loop we can stop the game engine:
    pygame.quit()


#if __name__ == "__main__":
    # create the board
    #mainGame()
    
