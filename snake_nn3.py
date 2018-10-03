'''
Skynet Bot Neural Network System v1.01

This utilizes tflearn based on Tensor Flow for Python 3.6

ARGS:
-o filename |--open filename | Opens an existing neural network file for use.
-e filename |--export filename | Export new neural net to this file.
-g true/false | --gui true/false | Show the game's GUI, or only text results.
-i int | --initial_games int | Amount of initial test set generation. 
-t int | --test_games int | Amount of games to run against the training set.030.


Training will be done with a dataset in CSV format for now. Later we can use more complex methods.


We can gather initial data by randomly running the snake game, and acquiring histories of inputs.
For each move, we can capture everything the snake "sees" and refer back to it later.
So: for Step 1: snake_observations[(0,1,1,3)

A dataset will have the following shape:
1,0,1,1,3 
0,0,1,1,2
1,0,1,2,3

To provide vision to the immediate left, front, right, and back of the snake, as well
as the suggested move (0, 1, 2, or 3 to represent direction choice.)

When this is ran through the neural network, the inputs (1,0,1,2 - not the last element!) will
be inputted into the NN's "sensors" - one for each value, or feature. These will then pass through
a hidden layer in the NN, using TFLearn, and return an output (0,1,2, or 3 to represent movement choice.)


'''

from snake import SnakeGame
from random import randint
import numpy as np
import tflearn
import math
import argparse
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter

class SnakeNN3:
    def __init__(self, initial_games = 100, test_games = 100, goal_steps = 100, lr = 0.01, filename = 'snake_nn3.tflearn'):
            self.initial_games = initial_games
            self.test_games = test_games
            self.goal_steps = goal_steps
            self.lr = lr
            self.filename = filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enter a filename to parse.")
    parser.add_argument("-o", "--open", required=False, help="filename of network to open for use.")
    parser.add_argument("-e", "--export", required=False, help="filename to save network in")
    args = parser.parse_args()
    
    filename = args.filename
    SnakeNN3().start(args.filename)