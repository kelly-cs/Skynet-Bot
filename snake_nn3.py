'''
Skynet Bot Neural Network System v1.01

This utilizes tflearn based on Tensor Flow for Python 3.6

ARGS:
-o filename |--open filename | Opens an existing neural network file for use.
-e filename |--export filename | Export new neural net to this file.
-g true/false | --gui true/false | Show the game's GUI, or only text results.
-i int | --initial_games int | Amount of initial test set generation. 
-t int | --test_games int | Amount of games to run against the training set.030.
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
            self.vectors_and_keys = [
                    [[-1, 0], 0],
                    [[0, 1], 1],
                    [[1, 0], 2],
                    [[0, -1], 3]
                    ]    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enter a filename to parse.")
    parser.add_argument("-f", "--filename", required=True, help="filename to save network in")
    args = parser.parse_args()
    
    filename = args.filename
    SnakeNN3().start(args.filename)