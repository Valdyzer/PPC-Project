import pygame
import sys
from main import Joueur

# Initialisation de Pygame
pygame.init()

# Créer la fenêtre 
largeur, hauteur = 700, 400
taille_fenetre = (largeur, hauteur)
fenetre = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption('Hannabis')

couleur_fond = (70, 134, 71)
couleur_rectangles = (255, 255, 255)
couleur_texte = (0, 0, 0)


# Position et taille des rectangles
start_button = pygame.Rect(200, 250, 300, 75)
start_text = "JOIN GAME"
police = pygame.font.Font(None, 40)  # Utiliser une police par défaut de taille 36

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 --> clic gauche
        # Vérifier si le clic est à l'intérieur de l'un des rectangles
            if start_button.collidepoint(event.pos):
                print(f"Clic sur le rectangle")

    # Effacer l'écran
    fenetre.fill(couleur_fond)

    # Dessiner les rectangles
    pygame.draw.rect(fenetre, couleur_rectangles, start_button)

    # Créer une surface de texte
    texte_surface = police.render(start_text, True, couleur_texte)

    # Obtenir le rectangle entourant la surface de texte
    texte_rect = texte_surface.get_rect()

    # Centrer le texte dans le rectangle
    texte_rect.center = start_button.center

    # Dessiner le texte dans la fenêtre
    fenetre.blit(texte_surface, texte_rect)


    # Mettre à jour l'affichage
    pygame.display.flip()

    # Ajustement des IPS
    pygame.time.Clock().tick(30)
