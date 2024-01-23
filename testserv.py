import socket
from multiprocessing import Process

def client_handler(s, a):
    with s:
        print("Connected to client: ", a)
        data = s.recv(1024)
        while len(data):
            s.sendall(data)
            data = s.recv(1024)
        print("Disconnecting from client: ", a)
            
HOST = "localhost"
PORT = 7776
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(4)
    while True:
        client_socket, address = server_socket.accept()
        p = Process(target=client_handler, args=(client_socket, address))
        p.start()