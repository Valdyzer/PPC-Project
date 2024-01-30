# client
import socket
import art
from colorama import init, Fore
import re


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
    

def treat_view(msg):

    #divide into sentences for each player
    lines = msg.split("\n")

    #remove the empty last line
    lines.pop()

    #search for something starting and ending with () and has a string then , then an int
    pattern = re.compile(r"\('(.*?)', (\d+)\)")

    for line in lines:

        parts = line.split(":")

        matches = pattern.findall(parts[1])

        print(f"{parts[0]} : ")

        for match in matches:
            view_color(match)

        print(Fore.RESET + "")




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

                received_info = client_socket.recv(1024).decode()
                treat_view(received_info)


            elif action == "play":
                carte = action + " " + input("Quelle carte veut-tu jouer ? ")
                client_socket.sendall(carte.encode())
                player_turn = False

            else:
                print("INCORRECT !! Choisissez une des actions proposées ci-dessus.")
                continue