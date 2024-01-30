# client
import socket
import art
from colorama import init, Fore


def view_color(tab):
    if tab[0]=="ROUGE":
        print(Fore.RED + "\t" + tab[1], end="")
    elif tab[0]=="BLEU":
        print(Fore.BLUE + "\t" + tab[1], end="")
    elif tab[0]=="VERT":
        print(Fore.GREEN + "\t" + tab[1], end="")
    elif tab[0]=="JAUNE":
        print(Fore.YELLOW + "\t" + tab[1], end="")
    elif tab[0]=="BLANC":
        print(Fore.WHITE + "\t" + tab[1], end="")
    else:
        return



init()  # initialisation de la librairie "colorama"
pseudo = input("Input your player name: ")
PORT = int(input("Put the game port: "))
HOST = "localhost"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(pseudo.encode())
    action = "no"
    while action.lower() != "yes":

        action = input("Are you ready ? ").lower()
        client_socket.sendall(action.encode())

    
    art.tprint("\n\n\nHANNABIS","rnd-large")
    print("\nHanabi est un jeu de cartes coopératif dans lequel les joueurs travaillent ensemble pour créer une suite complète de cartes de couleurs. Voici une brève explication des règles du jeu.\n")
    print("Objectif : L'objectif principal est de jouer toutes les cartes dans l'ordre correct (de 1 à 5) et par couleur.")
    print("Le jeu contient des cartes de cinq couleurs (rouge, jaune, vert, bleu, blanc) et des numéros de 1 à 5 pour chaque couleur. Chaque joueur reçoit une main de cinq cartes qu'il ne peut pas voir (Vous ne pouvez pas regarder vos propres cartes).")
    print("Les joueurs peuvent donner des indices aux autres joueurs pour les aider à jouer leurs cartes. Les indices sont donnés sur la couleur ou le numéro d'une carte spécifique.")
    print("Les joueurs peuvent jouer une carte de leur main, mais ils doivent suivre l'ordre numérique et par couleur. Si la carte est correctement jouée, elle s'ajoute à l'une des pile de couleur. Prêt ? C'EST PARTI !\n\n")
    while True:

        received_info = client_socket.recv(1024)
        print(received_info.decode())
        player_turn = True
        
        while player_turn:

            action = input("\nQuelle action choisis-tu ? ").lower()

            if action == "view":
                client_socket.sendall(action.encode())
                while True:
                    received_info = client_socket.recv(1024).decode()
                    if received_info == "STOP":
                        print(Fore.RESET + "")
                        break
                    print(received_info, end="")
                    while True:
                        card = client_socket.recv(1024).decode()
                        if card == "END":
                            print(Fore.RESET + "")
                            break
                        card = card.split(",")
                        view_color(card)


            elif action == "play":
                client_socket.sendall(action.encode())
                carte = input("Quelle carte veut-tu jouer ? ")
                client_socket.sendall(carte.encode())
                player_turn = False

            else:
                print("INCORRECT !! Choisissez une des actions proposées ci-dessus.")
                continue