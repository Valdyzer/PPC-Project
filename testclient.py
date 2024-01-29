# client
import socket
import art


HOST = "localhost"

pseudo = input("Input your player name: ")
PORT = int(input("Put the game port: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(pseudo.encode())
    action = "no"
    while action.lower() != "yes":

        action = input("Are you ready ? ").lower()
        client_socket.sendall(action.encode())

    
    art.tprint("\n\n\nHANNABIS","rnd-xlarge")
    print("\nHanabi est un jeu de cartes coopératif dans lequel les joueurs travaillent ensemble pour créer une suite complète de cartes de couleurs. Voici une brève explication des règles du jeu.\n")
    print("Objectif : L'objectif principal est de jouer toutes les cartes dans l'ordre correct (de 1 à 5) et par couleur.")
    print("Le jeu contient des cartes de cinq couleurs (rouge, jaune, vert, bleu, blanc) et des numéros de 1 à 5 pour chaque couleur. Chaque joueur reçoit une main de cinq cartes qu'il ne peut pas voir (Vous ne pouvez pas regarder vos propres cartes).")
    print("Les joueurs peuvent donner des indices aux autres joueurs pour les aider à jouer leurs cartes. Les indices sont donnés sur la couleur ou le numéro d'une carte spécifique.")
    print("Les joueurs peuvent jouer une carte de leur main, mais ils doivent suivre l'ordre numérique et par couleur. Si la carte est correctement jouée, elle contribue s'ajoute à l'une des suite de couleur. Prêt ? C'EST PARTI !\n\n")
    while True:

        received_info = client_socket.recv(1024)
        print(received_info.decode())
        player_turn = True
        
        while player_turn:

            action = input("Action ? ").lower()

            if action == "view":
                client_socket.sendall(action.encode())
                received_info = client_socket.recv(1024)
                print(received_info.decode())

            elif "play" in action:
                client_socket.sendall(action.encode())
                player_turn = False

            else:
                print("INCORRECT !! Choisissez une des actions proposées ci-dessus.")
                continue