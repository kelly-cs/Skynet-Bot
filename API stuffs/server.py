import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
CLIENT_PORT = 5006
MESSAGE = "Wassup my homies!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


while True:
    data, addr = sock.recvfrom(1024)
    print ("received message: ", data.decode())
    sock.sendto(MESSAGE.encode(), (UDP_IP, CLIENT_PORT))

    
    

