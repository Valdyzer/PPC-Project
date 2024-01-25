# client
import socket
import pickle

HOST = "localhost"

pseudo = input("Input your player name: ")
PORT = int(input("Put the game port: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(pseudo.encode())
    action = "no"
    while action.lower() != "yes":

        action = input("Are you ready?").lower()
        client_socket.sendall(action.encode())
    
    while True:

        action = input("Action?").lower()
        client_socket.sendall(action.encode())

        received_info = client_socket.recv(1024)
        print(received_info.decode())