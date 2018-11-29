import math
import socket
import json
from snake import SnakeGame
from random import randint
import numpy as np
'''
Skynet Bot NN System
Supervised Learning
This version implements the first iteration of our API. The SERVER (Game) will prepare for a client to connect to start playing.

We receive lists from the NN/CLIENT, and excecute the actions in our game. 
We continually send observations to the NN/CLIENT so that they can, in turn, send us a JSON List 
that represents an action they want to perform. We repeat this cycle until the game ends.

CODES WE RECEIVE FROM CLIENT:
0 - connecting | our indication to start the game. No other data is sent.
1 - action | this indicates the client is sending us an action for us to execute.
2 - quitting | this indicates the client is quitting. We should end the game gracefully. 

CODES WE SEND:
2 - game is complete, will restart 
1 - game in process | send a list of observations with this code.
0 - game is complete, no restart | pair with an extra value that indiciates how well the AI did.
-1 - not available | no extra data to send. Default state.


'''
SERVER_IP = "127.0.0.1" # That's Me!
CLIENT_IP = "127.0.0.1"
connected = False
in_progress = False
IN_PORT = 50055 # server receives data here - IN
OUT_PORT = 50066 # server sends data here - OUT
OBSERVATION_LIST = [-1]
SEND_LIST = [-1]
active = True
game_counter = 1
MODE = 1 # 0 = text, 1 = visualize




def generate_observation(snake, food, obstacles):
    snake_direction = get_snake_direction_vector(snake)
    food_direction = get_food_direction_vector(snake, food)
    barrier_left = is_direction_blocked(snake, turn_vector_to_the_left(snake_direction), obstacles)
    barrier_front = is_direction_blocked(snake, snake_direction, obstacles)
    barrier_right = is_direction_blocked(snake, turn_vector_to_the_right(snake_direction), obstacles)
    angle = get_angle(snake_direction, food_direction)
    return np.array([int(barrier_left), int(barrier_front), int(barrier_right), str(angle)])

###################################################
# GAME SPECIFIC FUNCTIONS                         #
###################################################
def add_action_to_observation(observation, action):
    return np.append([action], observation)

def get_snake_direction_vector(snake):
    return np.array(snake[0]) - np.array(snake[1])

def get_food_direction_vector(snake, food):
    return np.array(food) - np.array(snake[0])
    
def normalize_vector(vector):
    return vector / np.linalg.norm(vector)

def get_food_distance(snake, food):
    return np.linalg.norm(get_food_direction_vector(snake, food))

def is_direction_blocked(snake, direction, obstacles):
    point = np.array(snake[0]) + np.array(direction)
    return(point.tolist() in snake[:-1] or point[0] == 0 or point[1] == 0 or point[0] == 21 or point[1] == 21 or (point.tolist() in obstacles))

def turn_vector_to_the_left(vector):
    return np.array([-vector[1], vector[0]])

def turn_vector_to_the_right(vector):
    return np.array([vector[1], -vector[0]])

def get_angle(a, b):
    a = normalize_vector(a)
    b = normalize_vector(b)
    return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1]) / math.pi


def get_game_action(snake, action):
    print("snake: " + str(snake))
    print("random action: " + str(action))
    snake_direction = get_snake_direction_vector(snake)
    new_direction = snake_direction
    if action == -1:
        new_direction = turn_vector_to_the_left(snake_direction)
    elif action == 1:
        new_direction = turn_vector_to_the_right(snake_direction)
    for pair in vectors_and_keys:
        if pair[0] == new_direction.tolist():
            game_action = pair[1]
    return game_action

def generate_action(snake):
    action = make_prediction(0,2) - 1
    return get_game_action(snake, action)        

###################################################


# this will perform necessary steps to start the game and get it ready to perform, and return any values we will be manipulating.
# will return these values as a list.
def start_game(game): # this s passed by reference, so us starting the game within the function should work globally.
    a, b, c, d, e = game.start() # steps, prev_score, snake (a list), food (x,y), obstacles (list of x,y pairs).
    return [a,b,c,d,e] # will vary based on game. These are the things we will be using to train the neural net later.
    

while active:
    # Create a Game object and get it ready.
    print("Initializing the game.")
    if(MODE == 1):
        game = SnakeGame(gui = True)
    elif(MODE == 0):
        game = SnakeGame()
    print("Game initialized.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, IN_PORT)) # bind the incoming port. 
    print("Waiting for Client.")
    
    while not connected:
        try:
            data, addr = sock.recvfrom(1024)
            received_json = json.loads(data)
            if(received_json[0] == 0): # if client's code is "connecting"
                connected = True
                in_progress = True
                print("Client has connected: " + str(addr))
                print("Starting Game.")
                start_game(game)
        except Exception as e:
            print("An error occurred initialization." + str(e))

    while in_progress:
        try:
            # acquire observations from game, as a list.
            OBSERVATION_LIST = game.generate_observations_as_list() # get a list of observations
            #OBSERVATION_LIST = generate_observation(OBSERVATION_LIST[2], OBSERVATION_LIST[3], OBSERVATION_LIST[4])
            
            # send observations to client
            if(OBSERVATION_LIST[0] == True): # if we have the "DONE" marker of our game.
                SEND_LIST = [0,OBSERVATION_LIST] # remember: we talk in [code, [obs1,obs2,obs3....]] form.
                sock.sendto((json.dumps(SEND_LIST)).encode(), (CLIENT_IP, OUT_PORT)) 
                print("sending ENDGAME message! " + str(SEND_LIST))
                game.end_game()
            else:
                SEND_LIST = [1,OBSERVATION_LIST] # remember: we talk in [code, [obs1,obs2,obs3....]] form.
                sock.sendto((json.dumps(SEND_LIST)).encode(), (CLIENT_IP, OUT_PORT)) 


            print("sent message " + str(SEND_LIST))
            # we wait for client's response.
            data, addr = sock.recvfrom(1024) 
            # process the response, perform the action in-game.
            print ("received message: ", data.decode())
            received_json = json.loads(data)
            if(received_json[0] == 1):
                game.step(received_json[1]) # input the action into our game and proceed.
            elif(received_json[0] == 2):
                game.end_game()
                #active = false
                in_progress = false
                connected = false
                print("Client is disconnecting. Exiting game.")
                exit()
            elif(received_json[0] == 0):
                print("WARNING: A client is connecting, even though game is in progress!")
            else:
                print("An unknown response was received from the client!")
                print("RECEIVED: " + str(received_json))

        except Exception as e:
            print("An Error has occurred: " + str(e))
            exit()
    
    print("Game " + str(game_counter) + " completed. Looping back to start of program.")

print("All finished! Quitting...")
exit()
    
    


