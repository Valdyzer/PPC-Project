import socket
from multiprocessing import Process, Value, Manager

COULEURS = ["ROUGE", "BLEU", "VERT", "JAUNE", "BLANC"]

class Game:
    def __init__(self, manager):
        self.CARDS_PER_PLAYER = 5
        self.fuse_token = 3
        self.info_token = 0
        self.nb_players = Value("i",0)
        
        self.player_list = manager.list()
        self.ready_player_list = manager.list()
        self.host = "Localhost"
        self.port = 0

        self.set_up_server()

    def available_place(self):
        return self.nb_players.value < 5

    def add_player(self, player_name):
        self.nb_players.value += 1
        self.player_list.append(player_name)

    def remove_player(self, player_name):
        self.nb_players.value -= 1
        self.player_list.remove(player_name)
        self.ready_player_list.append(player_name)

    def add_ready_player(self, player_name):
        self.ready_player_list.append(player_name)

    def set_up_server(self):
        self.port = int(input("Input the game port: "))

        




def client_handler(s, a):
    with s:
        client_playername = (s.recv(1024)).decode()
        
        server.add_player(client_playername)
        print(f"{client_playername} connected with the address: {a}")
        print("Number of players: ", server.nb_players.value)
        print(f"List of connected players: {server.player_list}")

        player_ready = "not empty"
        while player_ready != "":

            player_ready = s.recv(1024).decode()

            if(player_ready.lower() == "yes"):
                print(f"{client_playername} is ready.")
                server.add_ready_player(client_playername)



        server.remove_player(client_playername)
        print(f"{client_playername} disconnected with the address: {a}")
        print("Number of players: ", server.nb_players.value)
        print(f"List of connected players: {server.player_list}")



waitingForPlayers = True

with Manager() as manager:

    server = Game(manager)


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server.host, server.port))
        server_socket.listen(1)
        server_socket.setblocking(False)


        while waitingForPlayers:
            if len(server.ready_player_list) == len(server.player_list) and len(server.player_list) > 1:
                print(f"{server.player_list}               {server.player_list}")
                waitingForPlayers = False

            try:
                if server.available_place():
                    client_socket, address = server_socket.accept()

                    print("Number of players: ", server.nb_players.value)
                    p = Process(target=client_handler, args=(client_socket, address))
                    p.start()
            
            except BlockingIOError:
                pass

        