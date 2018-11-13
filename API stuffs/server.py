import socket
import json

'''
We receive lists from the NN/CLIENT, and excecute the actions in our game. 
We continually send observations to the NN/CLIENT so that they can, in turn, send us a JSON List 
that represents an action they want to perform. We repeat this cycle until the game ends.

CODES WE RECEIVE FROM CLIENT:
0 - connecting | our indication to start the game. No other data is sent.
1 - action | this indicates the client is sending us an action for us to execute.
2 - quitting | this indicates the client is quitting. We should end the game gracefully. 

CODES WE SEND:
1 - game in process | send a list of observations with this code.
0 - game is complete | pair with an extra value that indiciates how well the AI did.
-1 - game has not started | no extra data to send. Default state.


'''
SERVER_IP = "127.0.0.1" # That's Me!
CLIENT_IP = "127.0.0.1"
connected = False
in_progress = False
IN_PORT = 50055 # server receives data here - IN
OUT_PORT = 50066 # server sends data here - OUT
OBSERVATION_LIST = [-1]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, IN_PORT)) # bind the incoming port. 
print("Waiting for Client.")


# actual processing will take place here later. 
def get_observations():
    obs = []
    obs = [1,[1,0,1]]
    return obs
    
while not connected:
    try:
        data, addr = sock.recvfrom(1024)
        received_json = json.loads(data)
        if(received_json[0] == 0): # if client's code is "connecting"
            connected = True
            in_progress = True
            print("Client has connected: " + str(addr))
            print("Starting Game.")
    except Exception as e:
        print("An error occurred initially connecting to the client. Restarting.")
        
while in_progress:
    try:
        # acquire observations from game.
        OBSERVATION_LIST = get_observations()
        sock.sendto((json.dumps(OBSERVATION_LIST)).encode(), (CLIENT_IP, OUT_PORT)) # send observations to client
        print("sent message " + str(OBSERVATION_LIST))
        data, addr = sock.recvfrom(1024) # we wait for client's response.
        # process the response, perform the action in-game.
        print ("received message: ", data.decode())
        received_json = json.loads(data)
        
        exit()
    except Exception as e:
        print("An Error has occurred: " + str(e))
        exit()
    
    

