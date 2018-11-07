import numpy as np
import tflearn
from sky_nn_supp import *
import math
import argparse
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter

snake = [[10,10],[11,10],[12,10]]
obstacles = [[12,15], [9,10], [13,13]]
snake_direction_vector = np.array(snake[0]) - np.array(snake[1])

point = np.array(snake[0]) + snake_direction_vector
print("POINTY:")
print(point)
print(point.tolist() in snake[:-1] or point[0] == 0 or point[1] == 0 or point[0] == 21 or point[1] == 21 or
(point.tolist() in obstacles))


	