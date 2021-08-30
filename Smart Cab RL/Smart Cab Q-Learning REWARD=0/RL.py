# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 04:26:29 2021

@author: wasil
"""

import smart_cab_adapted as sc
from collections import defaultdict

import numpy as np
import pickle

alpha    = 0.1
discount = 1
Q=defaultdict(lambda: [0,0,0,0])

gamecounter = 0

PASSENGER_POS = [[0, 0], [4, 0], [0, 4], [4, 3]]

def get_states(I, J, p_I, p_J, dropoff_position):
    """
    A state space is:
    (taxis_row, taxis_col, passengers_location, destination)
    All would be single digit numbers.
    """
    #print(I, J, pickup_position, dropoff_position)
    return str(I)+"_"+str(J)+"_"+str(p_I)+"_"+str(p_J)+"_"+str(dropoff_position)

oldState = None
oldAction = None

Q_trained = 0

def counter(input_):
    global gamecounter
    print("######################################### ----> ", gamecounter)
    if( input_ != "RUN"):
        if gamecounter % 100_000 == 0:
            print("Saved")
            with open("QLearning-SmartCab" + str(gamecounter) + ".pickle", "wb") as file:
                pickle.dump(dict(Q), file)
        
    gamecounter += 1
    
reward_list = []
counter_list = 0
def get_actions(I, J, p_I, p_J, dropoff_position, REWARD):
    global counter_list
    global reward_list
    
    global oldState
    global oldAction
    
    newstate = get_states(I, J, p_I, p_J, dropoff_position)
    
    estReward = Q[newstate] 
    prevReward = Q[oldState]
    
    index = None

    # select action
    if oldAction == "down":
        index = 0
    elif oldAction == "up":
        index = 1
    elif oldAction == "right":
        index = 2
    else:
        index = 3
    
    prevReward[index] = (1 - alpha) * prevReward[index] + alpha * (REWARD + discount * max(estReward))
    Q[oldState] = prevReward
    
    oldState = newstate
    
    index = np.argmax(np.array(estReward))
        
    if index == 0:
        oldAction = "down"
        return "DOWN"
    elif index == 1:
        oldAction = "up"
        return "UP"
    elif index == 2:
        oldAction = "right"
        return "RIGHT"
    elif index == 3:
        oldAction = "left"
        return "LEFT"

def run(I, J, p_I, p_J, dropoff_position):
    state = get_states(I, J, p_I, p_J, dropoff_position)
    estReward = Q_trained[state]
    
    index = np.argmax(np.array(estReward))
    if index == 0:       
        return "DOWN"
    elif index == 1:        
        return "UP"
    elif index == 2:        
        return "RIGHT"
    elif index == 3:
        return "LEFT"

if __name__ == "__main__":
    input_ = input("Enter 'TRAIN' to train or 'RUN' to run the game:")
    if input_ == "RUN":
        # read the trained Q dictionary
        with open("QLearning-SmartCab500000"+".pickle", "rb") as file:
            Q_trained = pickle.load(file)
    
    # create the board
    sc.mainGame(get_actions, counter, run, input_)