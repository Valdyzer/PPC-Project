import socket
import random
from multiprocessing import Process, Value, Manager
from multiprocessing.managers import BaseManager
from threading import Thread
import sysv_ipc
import signal

COULEURS = ["ROUGE", "BLEU", "VERT", "JAUNE", "BLANC"]

class Game:
    def __init__(self, manager):
        self.CARDS_PER_PLAYER = 5
        self.fuse_token = Value("i",3)
        self.info_token = 0
        self.tour_nb = Value("i",-1)
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
            self.all_players_cards[player[0]] = []

            for i in range(self.CARDS_PER_PLAYER):
                self.distribute_cards(player[0])


            print(f"To player {player[0]} are given: {self.all_players_cards[player[0]]}.")


        shared_memory.update({"game_status":self.game_status})
        shared_memory.update({"game_status":"Playing"})
        shared_memory.update({"liste_joueurs":list(game.player_list)})
        shared_memory.update({"information_tokens":game.info_token})
        shared_memory.update({"fuse_tokens":game.fuse_token})
        shared_memory.update({"construction":dict(game.track)})

        #Pour start la game
        self.prochain_tour()


    def distribute_cards(self,player):
        if len(self.pioche) > 0:
            ancienne_main = self.all_players_cards[player]

            card_picked = self.pioche.pop()
            ancienne_main.append(card_picked)

            self.all_players_cards[player] = ancienne_main


    def prochain_tour(self):
        self.tour_nb.value = (self.tour_nb.value + 1) % self.nb_players.value
        playing_player = self.ready_player_list[self.tour_nb.value][0]
        playing_player_socket = self.ready_player_list[self.tour_nb.value][1]
        print(f"C'est le tour de {playing_player}.")

        message_a_envoye = "Les piles présentes sur la table sont: "
        for couleur, nb in self.track.items():
            message_a_envoye += f"{couleur} -> {nb}   "

        message_a_envoye += "\nTes actions possibles sont : \n - view (regarder les cartes de tous les joueurs),\n - play (poser une carte),\n - hint (donner un indice à un joueur),\n - lookup (consulter les indices)."
        playing_player_socket.sendall(message_a_envoye.encode())


    def valid_card(self,played_card):
        played_card_couleur = played_card[0]
        played_card_nb = played_card[1]

        if self.track[played_card_couleur] == played_card_nb-1:
            return True
        else:
            return False


    def poser_carte(self, player_name, played_card_nb):

        played_card = self.all_players_cards[player_name][played_card_nb-1]
        print(f"{player_name} played the card: {played_card}.")
        self.remove_card(player_name,played_card_nb-1)

        if self.valid_card(played_card):
            self.track[played_card[0]] += 1
            print(f"{player_name} was correct.")
            self.distribute_cards(player_name)
            shared_memory.update({"construction":dict(self.track)})

            self.check_win()

        else:
            self.fuse_token.value -= 1
            shared_memory.update({"fuse_tokens":self.fuse_token.value})
            print(f"{player_name} was wrong, you loose 1 fuse token. You have {shared_memory.get('fuse_tokens')} left.")
            self.distribute_cards(player_name)

            self.check_loose()



    def remove_card(self,player,index):
        ancienne_main = self.all_players_cards[player]
        ancienne_main.pop(index)
        self.all_players_cards[player] = ancienne_main


    def run_server(shared_memory):
        manager = BaseManager(address=('localhost', 50000), authkey=b'test')
        server_shared_memory = shared_memory
        manager.get_shared_memory = lambda: server_shared_memory
        server = manager.get_server()
        server.serve_forever()

    
    def declencher_prochain_thread_end(self,name):

        filtered_list = [tup for tup in self.ready_player_list if tup[0] != name]

        if len(filtered_list) > 0:
            
            if(self.fuse_token.value <= 1):
                filtered_list[0][1].sendall("ENDOFGAMELOSS".encode())
            else:
                filtered_list[0][1].sendall("ENDOFGAMEWIN".encode())


            


    def check_win(self):
        for pile, nb in self.track.items():
            if nb < 5:
                return False

        self.game_status = "Victory"
        shared_memory.update({"game_status":self.game_status})  
        return True
    
    def check_loose(self):
        if self.fuse_token.value <= 0:
            self.game_status = "GameOver"
            shared_memory.update({"game_status":self.game_status})
            return True
        else:
            return False
    



def client_handler(s, a):
    with s:
        client_playername = (s.recv(1024)).decode()
        
        game.add_player(client_playername)
        print(f"{client_playername} connected with the address: {a}")
        print("Number of players: ", game.nb_players.value)
        print(f"List of connected players: {game.player_list}")

        player_action = "not empty"

        # ready code
        while player_action != "":

            player_action = s.recv(1024).decode()

            if(player_action.lower() == "yes"):
                print(f"{client_playername} is ready.")
                game.add_ready_player(client_playername,s)
                break

        # during game code
        while shared_memory.get("game_status") == "Playing" or shared_memory.get("game_status") == "WaitingForPlayers":
            player_action = s.recv(1024).decode()

            # affiche les mains de tous les joueurs
            if(player_action.lower() == "view"):
                print(f"Sending view info to {client_playername}")

                info_string = ""
                for player, cards in game.all_players_cards.items():
                    if player != client_playername:
                        info_string += f"{player} has these cards : "

                        for i in range(len(cards)):
                            info_string += f"{game.all_players_cards[player][i]} "

                        info_string += "\n"
                print(info_string)
                s.sendall(info_string.encode())

            # pose une carte
            elif("play" in player_action.lower()):

                card_played_nb = int(player_action[-1])
                game.poser_carte(client_playername, card_played_nb)
            

                if game.fuse_token.value > 0:
                        game.prochain_tour()

            elif("hint" in player_action.lower()):

                print(f"{client_playername} sent a hint.")
                game.prochain_tour()

        print(game.fuse_token.value)
        if(game.fuse_token.value <= 1):
            print("loss")
            s.sendall("ENDOFGAMELOSS".encode())
        else:
            print("win")
            s.sendall("ENDOFGAMEWIN".encode())


        game.declencher_prochain_thread_end(client_playername)   

        while game.game_status == "Victory" or game.game_status == "GameOver":
                pass
     

        game.remove_player(client_playername)
        print(f"{client_playername} disconnected with the address: {a}")
        print("Number of players: ", game.nb_players.value)
        print(f"List of connected players: {game.player_list}")


if __name__ == "__main__":

    with Manager() as manager:

        key = 1234
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

        game = Game(manager)

        shared_memory = {"game_status": "WaitingForPlayers", "liste_joueurs": [], "information_tokens": 0, "fuse_tokens": 0, "construction": {}}

        BaseManager.register('get_shared_memory', callable=lambda: shared_memory)
        server_thread = Thread(target=game.run_server)
        server_thread.start()


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((game.host, game.port))
            server_socket.listen(1)
            server_socket.setblocking(False)


            while game.game_status == "WaitingForPlayers":
                if len(game.ready_player_list) == len(game.player_list) and len(game.player_list) > 1:
                    game.game_status = "Playing"

                try:
                    if game.available_place():
                        client_socket, address = server_socket.accept()

                        print("Number of players: ", game.nb_players.value)
                        t = Process(target=client_handler, args=(client_socket, address))
                        t.start()
                
                except BlockingIOError:
                    pass

            game.set_up_game()

            while game.game_status == "Playing":
                pass

        mq.remove()
