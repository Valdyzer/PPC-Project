import socket
import random
from multiprocessing import Process, Value, Manager
import pickle

COULEURS = ["ROUGE", "BLEU", "VERT", "JAUNE", "BLANC"]

class Game:
    def __init__(self, manager):
        self.CARDS_PER_PLAYER = 5
        self.fuse_token = 3
        self.info_token = 0
        self.track = manager.dict()
        self.pioche = manager.list()
        self.all_players_cards = manager.dict()
        self.game_status = "WaitingForPlayers"

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

        self.ready_player_list = [(name, other_data) for name, other_data in self.ready_player_list if name != player_name]


    def add_ready_player(self, player_name, s):
        self.ready_player_list.append((player_name, s))

    def set_up_server(self):
        self.port = int(input("Input the game port: "))

    def set_up_game(self):
        couleurs_choisis = random.sample(COULEURS, self.nb_players.value)

        for couleur in couleurs_choisis:
            self.track[couleur] = 0
            self.pioche += 3*[(couleur,1)] + 2*[(couleur,2)] + 2*[(couleur,3)] + 2*[(couleur,4)] + [(couleur,5)]
        
        self.info_token = self.nb_players.value + 3

        random.shuffle(self.pioche)

        for player in self.ready_player_list:
            cards_to_give = []

            for i in range(5):
                cards_to_give.append(self.distribute_cards())

            self.all_players_cards[player[0]] = cards_to_give

            print(f"To player {player[0]} are given: {cards_to_give}")


                

    def distribute_cards(self):

        if len(self.pioche) > 0:
            card_picked = self.pioche.pop()
            
            return card_picked 
    



def client_handler(s, a):
    with s:
        client_playername = (s.recv(1024)).decode()
        
        game.add_player(client_playername)
        print(f"{client_playername} connected with the address: {a}")
        print("Number of players: ", game.nb_players.value)
        print(f"List of connected players: {game.player_list}")

        player_action = "not empty"

        while player_action != "":

            player_action = s.recv(1024).decode()

            if(player_action.lower() == "yes"):
                print(f"{client_playername} is ready.")
                game.add_ready_player(client_playername,s)
                break


        while player_action != "":
            print("b")
            player_action = s.recv(1024).decode()

            if(player_action.lower() == "view"):
                print(f"Sending info to {client_playername}")
                sent_info = f"{game.all_players_cards[client_playername]}".encode()
                s.sendall(sent_info)

                

        game.remove_player(client_playername)
        print(f"{client_playername} disconnected with the address: {a}")
        print("Number of players: ", game.nb_players.value)
        print(f"List of connected players: {game.player_list}")



with Manager() as manager:

    game = Game(manager)


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((game.host, game.port))
        server_socket.listen(1)
        server_socket.setblocking(False)


        while game.game_status == "WaitingForPlayers":
            if len(game.ready_player_list) == len(game.player_list) and len(game.player_list) > 1:
                # print(f"{game.player_list}               {game.ready_player_list}")
                # print(f"{len(game.ready_player_list)}               {len(game.player_list)}")
                # print(f"{len(game.ready_player_list) == len(game.player_list)}")
                # print(f"{len(game.ready_player_list) == len(game.player_list) and len(game.player_list) > 1}")
                game.game_status = "GameLoop"

            try:
                if game.available_place():
                    client_socket, address = server_socket.accept()

                    print("Number of players: ", game.nb_players.value)
                    p = Process(target=client_handler, args=(client_socket, address))
                    p.start()
            
            except BlockingIOError:
                pass

        game.set_up_game()
        print(game.all_players_cards)

        while True:
            pass
