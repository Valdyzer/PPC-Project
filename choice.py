import random
from classes import Jeu,Joueur

COULEUR = ["ROUGE", "BLEU", "VERT", "JAUNE", "BLANC"]


def indice(partie):
    while True:
        liste = []
        checking = False

        print("\nA qui voulez-vous donner un indice ?")
        for i in range(partie.nb_players):
            print("-", partie.players[i].pseudo)
            liste.append(partie.players[i]) 
        n = input("\t")

        for i in range(partie.nb_players):
            if n == liste[i].pseudo:
                checking = True
                break

        if checking == True:
            while True:
                print("\nDe quoi traite cet indice :\t1 - Un numéro\t 2 - Une couleur")
                choix = int(input("\t"))
                nb = int(input("Nombre de carte à désigner : "))
                if choix == 1:
                    num = input("Numéro des cartes : ")
                    indice = "Tu as " + str(nb) + " cartes de comportant le numéro " + str(num) + "\n"
                    for i in range(partie.nb_players):
                        if n == liste[i].pseudo:
                            liste[i].indices.append(indice)
                    print(indice)
                    break
                if choix == 2:
                    couleur = input("Couleur des cartes : ")
                    indice = "Tu as " + str(nb) + " cartes de couleur " + couleur + "\n"
                    for i in range(partie.nb_players):
                        if n == liste[i].pseudo:
                            liste[i].indices.append(indice)
                    print(indice)
                    break
                else:
                    print("\nINCORRECT !!! Choisis parmis les paramètres proposés (indique son numéro)\n")
  
        else :
            print("\nINCORRECT !!! Ecrit le pseudo d'un joueur présent !\n")
        break

        



partie = Jeu()
partie.nb_players = int(input("\nNombre de joueur : "))         # Choisir 3 pour l'instant
partie.nb_colors = random.sample(COULEUR, partie.nb_players)
partie.nb_cards = 10 * partie.nb_colors
partie.info_token = partie.nb_players + 3
partie.track = {}
partie.pioche = []

for couleur in partie.nb_colors:
    partie.track[couleur] = 0
    partie.pioche += 3*[couleur+'_1'] + 2*[(couleur+'_2')] + 2*[(couleur+'_3')] + 2*[(couleur+'_4')] + [(couleur+'_5')]

print(partie.nb_colors)
print(partie.track)
print(partie.pioche)

p1 = Joueur()
partie.players.append(p1)
p2 = Joueur()
partie.players.append(p2)
p3 = Joueur()
partie.players.append(p3)

for i in range(len(partie.players)):
    print("\nPseudo du joueur", i+1, ":")
    partie.players[i].pseudo = input("\t")
    partie.players[i].deck = random.sample(partie.pioche, partie.CARDS_PER_PLAYERS)
    partie.players[i].order = i+1
    for j in range(partie.CARDS_PER_PLAYERS):
        partie.pioche.remove(partie.players[i].deck[j])


print("\n\n\n------------ HANNABIS --------------\n\n")
while True:
    print("A ton tour, choisis une action :")
    print("1 - Poser une carte")
    print("2 - Donner un indice à un joueur")
    # if len(p.indice) != 0:
    #   print("3 - Consulter les indices")
    choix = int(input("\t"))
    if choix == 1:
        # Pose()
        break
    elif choix == 2:
        indice(partie)
        break
    #elif (choix == 3) and (len(p.indice) != 0):
        # print(p.indice)
    else:
        print("INCORRECT !!! Choisis parmis les actions proposées (indique son numéro)")




