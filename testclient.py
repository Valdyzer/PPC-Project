# client
import socket
 
HOST = "localhost"

pseudo = input("Input your player name: ")
PORT = int(input("Put the game port: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(pseudo.encode())
    ready = "no"
    while True:
        #if ready.lower() != "no"
        pass