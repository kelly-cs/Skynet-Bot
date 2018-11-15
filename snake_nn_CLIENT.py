import socket
import json
import time

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
"game has not started" -1

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

CURRENT_GAME_DATA = [] # list of all observation/action pairs for a game. When game completes, they will be paired with a goal value.
MODE = 1 # MODES: 0 = Inactive, 1 = Data Population + Training (Supervised Learning), 2 = Model Testing
sock.bind((CLIENT_IP, IN_PORT)) # bind the incoming data port.


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
            if(MODE == 1): # data population AND training mode (supervised learning)
                # acquire the action to take from our NN, format as a json list.
                MSG_LIST[0] = 1 # code to indicate we are sending an action [ see above ]
                sock.sendto((json.dumps(MSG_LIST)).encode(), (SERVER_IP, OUT_PORT)) # send our action to the server.
                print("sending data: " + str(MSG_LIST))
            elif(MODE == 2): # Model Testing
                
                
        # TESTING MODE - USES THE NN TO GENERATE ACTIONS
        else:
            print("The game server is not ready yet. Waiting...")
        

        exit()
    except Exception as e:
        print("An Error has Occurred: " + str(e))
        exit()

    

    