import socket
from multiprocessing import Process, Value

COULEURS = ["ROUGE", "BLEU", "VERT", "JAUNE", "BLANC"]

class Game:
    def __init__(self):
        self.CARDS_PER_PLAYER = 5
        self.fuse_token = 3
        self.info_token = 0
        self.nb_players = Value("i",0)
        
        self.host = "Localhost"
        self.port = 0

        self.set_up_server()

    def available_place(self):
        return self.nb_players.value < 5

    def add_player(self):
        self.nb_players.value += 1

    def remove_player(self):
        self.nb_players.value -= 1

    def set_up_server(self):
        self.port = int(input("Input the game port: "))

        




def client_handler(s, a):
    with s:
        client_playername = (s.recv(1024)).decode()
        print(f"{client_playername} connected with the address: {a}")
        print("Number of players: ", server.nb_players.value)
        data = s.recv(1024)
        while len(data):
            s.sendall(data)
            data = s.recv(1024)

        server.remove_player()
        print(f"{client_playername} disconnected with the address: {a}")
        print("Number of players: ", server.nb_players.value)



waitingForPlayers = True

server = Game()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((server.host, server.port))
    server_socket.listen(1)


    while waitingForPlayers:

        if server.available_place():
            client_socket, address = server_socket.accept()
            server.add_player()
            print("Number of players: ", server.nb_players.value)
            p = Process(target=client_handler, args=(client_socket, address))
            p.start()