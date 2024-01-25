import pygame
import sys
import classes
from multiprocessing import Process
#from main import Joueur

def GAME():
    pygame.init()
    fenetre = pygame.display.set_mode([700, 400])
    pygame.time.Clock().tick(30)
    pygame.display.set_caption('Hannabis')

    couleur_fond = (70, 134, 71)
    couleur_rectangles = (255, 255, 255)
    couleur_texte = (0, 0, 0)


    # Position et taille des rectangles
    start_button = pygame.Rect(200, 250, 300, 75)
    start_text = "JOIN GAME"
    police = pygame.font.Font(None, 40)  # Utiliser une police de taille 40

    # Boucle principale
    click = 0 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 --> clic gauche
            # Vérifier si le clic est à l'intérieur de l'un des rectangles
                if start_button.collidepoint(event.pos):
                    print(click)
                    p = Process(target=PLAYER)
                    p.start()
                    click += 1

        # Effacer l'écran
        fenetre.fill(couleur_fond)

        pygame.draw.rect(fenetre, couleur_rectangles, start_button)
        texte_surface = police.render(start_text, True, couleur_texte)
        texte_rect = texte_surface.get_rect()
        texte_rect.center = start_button.center
        fenetre.blit(texte_surface, texte_rect)

        # Mettre à jour l'affichage
        pygame.display.flip()

def PLAYER():
    pygame.init()
    fenetre = pygame.display.set_mode([700, 400])
    pygame.time.Clock().tick(30)
    pygame.display.set_caption('Player')

    couleur_fond = (171, 196, 100)

    # Boucle principale
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        fenetre.fill(couleur_fond)
        pygame.display.flip()

