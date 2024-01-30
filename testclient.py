# client
import socket
from multiprocessing.managers import BaseManager
import art
from colorama import init, Fore
import sysv_ipc
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


def create_hint():
    hint_message = ""
    liste_joueurs = shared_memory.get("liste_joueurs")
    hint_type = len(liste_joueurs)
    print("\nA qui voulez-vous donner un indice ?")
    for player in liste_joueurs:
        if player != pseudo:
            print("-", player)

    hint_message = input("\t")

    while hint_message not in liste_joueurs:
        hint_message = input("Ce n'est pas un nom de joueur! Rééssaie:  ")

    print("\nDe quoi traite cet indice :\t1 - Un numéro\t 2 - Une couleur")

    message_cree = False

    while not message_cree:
        choix = int(input("\t"))
        if choix == 1:
            hint_message += " numero"
            hint_message += " " + input("Quel numéro? ")
            hint_message += " " + input("Quelles cartes sont concernées (séparées par une ,)? ")
            message_cree = True
        elif choix == 2:
            hint_message += " couleur"
            hint_message += " " + input("Quelle couleur? ")
            hint_message += " " + input("Quelles cartes sont concernées (séparées par une ,)? ")
            message_cree = True
        else:
            print("\nINCORRECT !!! Choisis parmis les paramètres proposés (indique son numéro)\n")
  

    return hint_message, hint_type


def treat_hint():
    print("Hints that have been sent this round:")
    hints_this_round = []

    first_message = ""
    t = -5
    if mq.current_messages > 0:
        first_message, t = mq.receive()
        hints_this_round.append((first_message,t))

        #send back the message loop condition
        mq.send(first_message,type=t)

    message = ""
    t1 = -5
    
    #recuperer tt les messages unes seule fois
    while mq.current_messages > 0:
        message, t1 = mq.receive()
        if message == first_message and t == t1:
            break

        else:
            hints_this_round.append((message,t))


    if len(hints_this_round) > 0:
        
        for hint in hints_this_round:
            msg = hint[0].decode()
            type = hint[1]

            #check if the hint made a full circle if not resend same hint with -1 type
            if type > 1:
                new_type = type - 1
                mq.send(msg,type=new_type)

            #treatement du hint et transformation en phrase
            elements = msg.split(" ")

            #check si ce hint concerne ce joueur
            if elements[0] == pseudo:
                elements[0] = "Your"

            phrase = ""
            if elements[1] == "numero":
                phrase = f"{elements[0]} only cards with number {elements[2]} are {elements[3]}."
            elif elements[1] == "couleur":
                phrase = f"{elements[0]} only {elements[2].lower()} cards are {elements[3]}."


            print(phrase)

init()  # initialisation de la librairie "colorama"
pseudo = input("Input your player name: ")
PORT = int(input("Put the game port: "))
HOST = "localhost"

key = 1234
mq = sysv_ipc.MessageQueue(key)

BaseManager.register('get_shared_memory')
m = BaseManager(address=('localhost', 50000), authkey=b'test')
m.connect()

shared_memory= m.get_shared_memory() 


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
        treat_hint()
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

            elif action == "hint":
                hint_message, t = create_hint()
                mq.send(hint_message.encode(),type=t)
                client_socket.sendall(action.encode())
                player_turn = False


            else:
                print("INCORRECT !! Choisissez une des actions proposées ci-dessus.")
                continue