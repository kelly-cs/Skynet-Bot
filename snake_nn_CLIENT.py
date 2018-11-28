import socket
import json
import time
import math
import tflearn
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
import numpy as np
from random import randint
'''
Skynet Bot NN System
Supervised Learning

 We send lists to the GAME/SERVER 

 ACTION CODES WE SEND: 
 "connecting" - 0  // send this again AFTER you receive a 0 code from the Server to restart multiple games for training.
 "action" - 1
 "quitting" - 2

 ACTIONS:
 A list of required instructions, output by the neural network. Can have any # of list elements.

 TYPE: JSON
 CONTENT: [ACTION CODE, [action instructions1,2,3,4,5.....]]
 EXAMPLE: ["action", [1,5,-2]] 
 USAGE: This will essentially instruct the game that the data being sent is in fact an action we wish it to perform.
        The data can represent anything, and it's not our job to necessarily care what it means -  it can vary.

RESPONSES WE RECEIVE:
The server will send us lists of observations regularly. We will then process those observations,
make a decision, and proceed this cycle until we receive an "end of game" code from the game.

RESPONSE CODES WE RECEIVE:
"game in process" 1
"game is complete" 0
"not available" -1

RESPONSE EXAMPLE:
[1, [observations]] ... e.g. [1, [1,5,-2,3....]]
or
[0, 4141]
[0, 0.5242]
We can use the data immediately after the response code to figure out things such as, "How well
did our AI do in reaching its goal?". 0 response codes will take all data retrieved in the testing process
and use it to re-evaluate weights it uses to make decisions. The goal the AI is trying to reach can be
specified to our NN before the process begins, and then we can use that data to help the AI make better
decisions later.
 
 FUTURE PLANS: To make this system more robust, and able to handle more complex instructions, it may make sense to
               nest multiple neural networks together to make more complex decisions independent of one another.
               So, for a real-time strategy game [say, starcraft] we could attempt a framework that does the following:
               
                    Main Strategy NN [Delegates Tasks]
                    | Micro NN             | Macro NN
                    + Makes Decisions      + Makes decisions based on "build orders"
                    Focused solely on unit   More broad decisionmaking 
                    control
                    

 
'''
CLIENT_IP = "127.0.0.1" # That's Me!
SERVER_IP = "127.0.0.1"

IN_PORT = 50066 # The port we receive data from the game/server with. - IN
OUT_PORT = 50055 # The port we send data to the game/server with. - OUT
MSG_LIST = [0, 'Connecting...'] # connecting
active = True
lr=0.001
filename = "snake_nn_2.tflearn"
test_gamaes = 1000
initial_games = 10000
goal = 2000


# kinda irrelevant - just for use in the snake game.
vectors_and_keys = [
                [[-1, 0], 0],
                [[0, 1], 1],
                [[1, 0], 2],
                [[0, -1], 3]
                ]

training_data = [] # this is where we will return training data to be used.
PREV_GAME_OBS = []
CURRENT_GAME_OBS = [] # list of all observation/action pairs for a game. When game completes, they will be paired with a goal value.
MODE = 1 # MODES: 0 = Inactive, 1 = Data Population + Training (Supervised Learning), 2 = Model Testing

def model():
    network = input_data(shape=[None, 5, 1], name='input') # shape of data [left, forward, right, angle, 

    # Activation and Regularization inside a layer:
    network = fully_connected(network, 25, activation='relu') # hidden layer neurons
    # Equivalent to:
    network = fully_connected(network, 1, activation='linear') # hidden layer neurons

    # Optimizer, Objective and Metric:        
    network = regression(network, optimizer='adam', learning_rate=lr, loss='mean_square', name='target')
    model = tflearn.DNN(network, tensorboard_dir='log')
    return model

def train_model(training_data, model):
    X = np.array([i[0] for i in training_data]).reshape(-1, 5, 1) # observations array
    y = np.array([i[1] for i in training_data]).reshape(-1, 1) # fitness value
    model.fit(X,y, n_epoch = 3, shuffle = True, run_id = filename)
    model.save(filename)
    return model

def generate_random_action():
    action = randint(0,2) - 1
    return action
    #return action, get_game_action(snake, action)


def generate_observation(snake, food, obstacles):
    snake_direction = get_snake_direction_vector(snake)
    food_direction = get_food_direction_vector(snake, food)
    barrier_left = is_direction_blocked(snake, turn_vector_to_the_left(snake_direction), obstacles)
    barrier_front = is_direction_blocked(snake, snake_direction, obstacles)
    barrier_right = is_direction_blocked(snake, turn_vector_to_the_right(snake_direction), obstacles)
    angle = get_angle(snake_direction, food_direction)
    return np.array([int(barrier_left), int(barrier_front), int(barrier_right), angle])

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

def make_prediction(observations, model, prev_observations):
    new_observations = generate_observation(observations[2],observations[3],observations[4])
    print(str(new_observations))
    predictions = []
    for action in range(-1,2):
        predictions.append(model.predict(add_action_to_observation(new_observations, action).reshape(-1, 5, 1))) # 5 is the number of observations we pass.
    return int(np.argmax(np.array(predictions)))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_IP, IN_PORT)) # bind the incoming data port.

print("loading nn")
nn_model = model()
nn_model.load(filename)
        
# initial connection
print("Connecting to Game Server at: " + SERVER_IP + ":" + str(OUT_PORT) + "...")
sock.sendto((json.dumps(MSG_LIST)).encode(), (SERVER_IP, OUT_PORT)) # inform the server we have connected.
# game step loop
while active: # while we're playing
    try:
        data, addr = sock.recvfrom(1024) # we wait for server's response.
        received_json = json.loads(data)
        print("data received:" + str(received_json))
        
        # If game is in progress, process data according to the mode we have selected.
        if(received_json[0] == 1): # if game is in progress, process observations.
            if(MODE == 1): # data population AND training mode [random actions, supervised results]
                CURRENT_GAME_OBS = received_json[1] # take in the list of observations
                #MSG_LIST[1] = generate_action(CURRENT_GAME_OBS[2]) # this is the snake.
                MSG_LIST[1] = get_game_action(CURRENT_GAME_OBS[2], make_prediction(CURRENT_GAME_OBS, nn_model, PREV_GAME_OBS) - 1) # see snake.py and snake_nn2.py from iteration 2 for reasoning
                print (MSG_LIST[1])
                # acquire the action to take from our NN, format as a json list.
                MSG_LIST[0] = 1 # code to indicate we are sending an action [ see above ]
                print (MSG_LIST[0])
                sock.sendto((json.dumps(MSG_LIST)).encode(), (SERVER_IP, OUT_PORT)) # send our action to the server.
                print("sending data: " + str(MSG_LIST))
            elif(MODE == 2): # Model Testing
                CURRENT_GAME_OBS = received_json[1] # take in the list of observations
                print(CURRENT_GAME_OBS)
                # acquire the action to take from our NN, format as a json list.
                MSG_LIST[0] = 1 # code to indicate we are sending an action [ see above ]
                print(MSG_LIST[0])
                sock.sendto((json.dumps(MSG_LIST)).encode(), (SERVER_IP, OUT_PORT)) # send our action to the server.
                print("sending data: " + str(MSG_LIST))
                # TESTING MODE - USES THE NN TO GENERATE ACTIONS
        else:
            print("The game server is not ready yet. Exiting...")
            break

    except Exception as e:
        print("An Error has Occurred: " + str(e))
        #exit()

    

    

