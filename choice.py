import random

COULEUR = ["ROUGE", "BLEU", "VERT", "JAUNE", "BLANC"]

nb_joueur = int(input())
couleurs_choisis = random.sample(COULEUR, nb_joueur)
track = {}
pioche = []


for couleur in couleurs_choisis:
    track[couleur] = 0

    pioche += 3*[couleur+'_1'] + 2*[(couleur,2)] + 2*[(couleur,3)] + 2*[(couleur,4)] + [(couleur,5)]


print(couleurs_choisis)
print(track)
print(pioche)
