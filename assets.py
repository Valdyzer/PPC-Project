import pygame
import sys
import classes
from multiprocessing import Process
#from main import Joueur

#def menu():
    

def GAME(connecting, start):
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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 --> clic gauche
            # Vérifier si le clic est à l'intérieur de l'un des rectangles
                if start_button.collidepoint(event.pos):
                    connecting.value += 1
                

        # Effacer l'écran
        fenetre.fill(couleur_fond)

        if start.value==0:
            pygame.draw.rect(fenetre, couleur_rectangles, start_button)
            texte_surface = police.render(start_text, True, couleur_texte)
            texte_rect = texte_surface.get_rect()
            texte_rect.center = start_button.center
            fenetre.blit(texte_surface, texte_rect)

        # Mettre à jour l'affichage
        pygame.display.flip()

def PLAYER():
    pygame.init() 
    pygame.time.Clock().tick(30) 
    fenetre = pygame.display.set_mode([700, 400]) 
    
    # basic font for user typed 
    base_font = pygame.font.Font(None, 36) 
    user_text = '' 
    
    # create rectangle 
    input_rect = pygame.Rect(200, 200, 140, 32) 
    
    couleur_fond = (171, 190, 100)

    color_active = pygame.Color('lightskyblue3') 
    
    # color_passive store color(chartreuse4) which is 
    # color of input box. 
    color_passive = pygame.Color('chartreuse4') 
    color = color_passive 
    
    active = False
    
    while True: 
        for event in pygame.event.get(): 
    
        # if user types QUIT then the screen will close 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                sys.exit() 
    
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False
    
            if event.type == pygame.KEYDOWN: 
    
                # Check for backspace 
                if event.key == pygame.K_BACKSPACE: 
    
                    # get text input from 0 to -1 i.e. end. 
                    user_text = user_text[:-1] 
    
                # Unicode standard is used for string 
                # formation 
                else: 
                    user_text += event.unicode
        
        # it will set background color of screen 
        fenetre.fill((couleur_fond)) 
    
        if active: 
            color = color_active 
        else: 
            color = color_passive 
            
        # draw rectangle and argument passed which should 
        # be on screen 
        pygame.draw.rect(fenetre, color, input_rect) 
    
        text_surface = base_font.render(user_text, True, (255, 255, 255)) 
        
        # render at position stated in arguments 
        fenetre.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
        
        # set width of textfield so that text cannot get 
        # outside of user's text input 
        input_rect.w = max(100, text_surface.get_width()+10) 
        
        # display.flip() will update only a portion of the 
        # screen to updated, not full area 
        pygame.display.flip() 
       