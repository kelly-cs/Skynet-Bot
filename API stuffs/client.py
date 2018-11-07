import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5006
SERVER_PORT = 5005
MESSAGE = "You ready?"

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    sock.sendto(MESSAGE.encode(), (UDP_IP, SERVER_PORT))
    data, addr = sock.recvfrom(1024)
    print("message received: ", data.decode())
    

    
    
