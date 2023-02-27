import pygame
import random
import os
from pygame import mixer

# initialisation de pygame et mixer
mixer.init()
pygame.init()

# dimensions de la fenêtre de jeu
ecran_width = 500 
ecran_height = 600 
# création de la fenêtre de jeu et lui donner un titre
ecran = pygame.display.set_mode((ecran_width, ecran_height))
pygame.display.set_caption("JumpyGump")

# cadence d'image définie à 60 images seconde
clock = pygame.time.Clock() 
FPS = 60 # images/seconde

# charger la musique et les sons
pygame.mixer.music.load("music&sons/silent.wav")
pygame.mixer.music.set_volume(0.6) # réglage du volume de la musique
pygame.mixer.music.play(-1, 0.0) # jouer en boucle
forrest_fx = pygame.mixer.Sound("music&sons/boing.wav") # charger le son du saut
forrest_fx.set_volume(0.4)
mort_fx = pygame.mixer.Sound("music&sons/plouf.wav") # charger le son de la mort du joueur
mort_fx.set_volume(0.5)

# variables du jeu
Scroll_thresh = 200 # distance à partir de laquelle l'écran commence à défiler
Gravity = 1 
Max_blocs = 10 # nombre maximum de blocs sur l'écran
scroll = 0 # défilement de l'écran
fond_scroll = 0 # défilement du fond
game_over = False # le jeu est terminé
score = 0 # score du joueur
fade_counter = 0 # compteur pour le fondu

if os.path.exists("score.txt"): # vérifier si le fichier score.txt existe
    with open("score.txt", "r") as file: # ouvrir le fichier score.txt en lecture
        high_score = int(file.read()) # récupérer le meilleur score
else:
    high_score = 0 # meilleur score

# définir les couleurs
white = (255, 255, 255)
black = (0, 0, 0)
panel = (0, 255, 0) # couleur du panneau d'information

# définir la police
font_small = pygame.font.SysFont("Comic Sans MS", 20)
font_big = pygame.font.SysFont("Comic Sans MS", 24)

# chargement des images
forest_image = pygame.image.load("img/forrest.png").convert_alpha() # charger l'image du joueur1
rambopiaf_image = pygame.image.load("img/rambopiaf.png").convert_alpha() # charger l'image du joueur2
fond_image = pygame.image.load("img/ville.jpeg").convert_alpha() # charger l'image de fond
fond_image = pygame.transform.scale(fond_image, (ecran_width, ecran_height)) # redimensionner l'image du fond
bloc_image = pygame.image.load("img/bloc.png").convert_alpha() # charger l'image du bloc

# fonction pour afficher le texte
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col) # créer une image avec le texte
    ecran.blit(img, (x, y)) # afficher l'image

# fonction pour dessiner le panneau d'information
def draw_panel():
    pygame.draw.rect(ecran, panel, (0, 0, ecran_width, 30)) # dessiner un rectangle
    pygame.draw.line(ecran, white, (0, 30), (ecran_width, 30), 2) # dessiner une ligne
    draw_text("SCORE: " + str(score), font_small, black, 0, 0) # afficher le score du joueur

# fonction pour dessiner le fond
def draw_fond(fond_scroll):
    ecran.blit(fond_image, (0, 0 + fond_scroll)) # afficher l'image du fond
    ecran.blit(fond_image, (0, -600 + fond_scroll)) # afficher l'image du fond en dessous

# classe du joueur
class Joueur():
    def __init__(self, x, y): # constructeur de la classe Joueur
        self.image = pygame.transform.scale(forest_image, (60, 60)) # redimensionner l'image du joueur
        self.width = 40 # largeur du rectangle du joueur
        self.height = 60 # hauteur du rectangle du joueur
        self.rect = pygame.Rect(0, 0, self.width, self.height) # rectangle du joueur pour la détection des collisions
        self.rect.center = (x, y) # position du joueur sur l'écran
        self.vel_y = 0 # vitesse de déplacement du joueur sur l'axe des y
        self.flip = False # l'orientation du joueur ne sera pas inversée

    def bouger(self): # déplacer le joueur
        # réinitialiser les variables de déplacement
        scroll = 0 # défilement de l'écran
        dx = 0 # déplacement sur l'axe des x
        dy = 0 # déplacement sur l'axe des y

        # récupérer les touches pressées
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]: # si la flèche gauche est pressée
            dx -= 10 # le joueur va vers la gauche
            self.flip = True # le joueur regarde vers la gauche grâce à la fonction flip
            # dans cette fonction, on inverse l'orientation de l'image du joueur
            # et dans mon cas, on voit les jambes de forrest changer de sens
        if key[pygame.K_RIGHT]: # si la flèche droite est pressée
            dx = 10 # le joueur va vers la droite
            self.flip = False # le joueur regarde vers la droite
            # et dans mon cas, on voit les jambes de forrest changer de sens

        # gérer la gravité
        self.vel_y += Gravity # augmenter la vitesse de déplacement du joueur sur l'axe des y
        dy += self.vel_y # déplacer le joueur sur l'axe des y

        # veiller à ce que le joueur ne sorte pas de l'écran
        if self.rect.left + dx < 0: # si le joueur sort de l'écran par la gauche
            dx = 0 - self.rect.left # le joueur ne peut pas aller plus loin que le bord gauche de l'écran
        if self.rect.right + dx > ecran_width: # si le joueur sort de l'écran par la droite
            dx = ecran_width - self.rect.right # le joueur ne peut pas aller plus loin que le bord droit de l'écran
        
        # vérifier si les blocs touchent le joueur
        for bloc in bloc_group: # parcourir la liste des blocs
            # vérifier si le joueur touche un rocher sur l'axe des y
            if bloc.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # vérifier si le joueur est au dessus du bloc
                if self.rect.bottom < bloc.rect.centery:
                    if self.vel_y > 0: # vérifier si le joueur est en train de tomber
                        self.rect.bottom = bloc.rect.centery # le joueur ne peut pas aller plus bas que le bloc
                        dy = 0 # le joueur ne tombe plus
                        self.vel_y = -20 # la vitesse de déplacement du joueur sur l'axe des y est réinitialisée
                        forrest_fx.play() # jouer le son du saut

        # vérifier si le joueur a rebondi en haut de l'écran
        if self.rect.top <= Scroll_thresh: # si le joueur est au dessus du seuil de défilement de l'écran
            if self.vel_y < 0: # si la vitesse de déplacement du joueur sur l'axe des y est négative
                scroll = -dy # le défilement de l'écran est égal à la valeur de déplacement du joueur sur l'axe des y

        # mettre à jour le rectangle du joueur
        self.rect.x += dx # déplacer le joueur sur l'axe des x
        self.rect.y += dy + scroll # déplacer le joueur sur l'axe des y et déplacer l'écran

        return scroll # retourner la valeur de défilement de l'écran   

    def draw(self): # afficher le joueur
        ecran.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 10, self.rect.y)) # afficher l'image du joueur
        pygame.draw.rect(ecran, white, self.rect, 1) # afficher le rectangle du joueur

class Bloc(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving): # constructeur de la classe Bloc
        pygame.sprite.Sprite.__init__(self) # initialiser la classe Sprite
        self.image = pygame.transform.scale(bloc_image, (width, 120)) # charger l'image du bloc et la redimensionner
        self.moving = moving # variable pour savoir si le bloc bouge
        self.move_counter = random.randint(0, 50) # variable pour le déplacement du bloc 
        self.direction = random.choice([-1, 1]) # variable pour la direction du déplacement du bloc (gauche ou droite)
        self.speed = random.randint(1, 2) # variable pour la vitesse du déplacement du bloc
        self.rect = self.image.get_rect() # récupérer le rectangle de l'image du bloc pour la détection des collisions
        self.rect.x = x # positionner le bloc sur l'axe des x
        self.rect.y = y # positionner le bloc sur l'axe des y

    def update(self, scroll): # mettre à jour le bloc
        if self.moving == True: # si le bloc bouge
            self.move_counter += 1 # augmenter le compteur de déplacement du bloc
            self.rect.x += self.direction * self.speed # déplacer le bloc sur l'axe des x dans la direction choisie à la vitesse choisie
        
        # vérifier si le bloc doit changer de direction
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > ecran_width: # si le compteur de déplacement du bloc est supérieur ou égal à 100 ou si le bloc sort de l'écran par la gauche ou la droite
            self.direction *= -1 # changer la direction du déplacement du bloc (gauche ou droite)
            self.move_counter = 0 # réinitialiser le compteur de déplacement du bloc

        # mettre à jour la position verticale du bloc
        self.rect.y += scroll

        # vérifier si le bloc sort de l'écran
        if self.rect.top > ecran_height: # si le bloc sort de l'écran par le haut
            self.kill() # supprimer le bloc

# créer le joueur
forrest = Joueur(ecran_width // 2, ecran_height - 100)

# créer les blocs
bloc_group = pygame.sprite.Group()

# créer les blocs de départ
bloc = Bloc(ecran_width // 2 -50, ecran_height - 100, 100, False)
bloc_group.add(bloc) # ajouter le bloc à la liste des blocs

# boucle de jeu
run = True # variable pour la boucle de jeu
while run:

    clock.tick(FPS) # définir la cadence d'image

    if game_over == False: # si le jeu n'est pas terminé
        scroll = forrest.bouger() # déplacer le joueur et récupérer la valeur de défilement de l'écran

        # affichage du fond
        fond_scroll += scroll # déplacer le fond sur l'axe des y en fonction de la valeur de défilement de l'écran
        if fond_scroll >= 600: # si le fond dépasse l'écran par le bas
            fond_scroll = 0 # réinitialiser le défilement du fond
        draw_fond(fond_scroll) # afficher le fond

        # affichage des blocs
        if len(bloc_group) < Max_blocs: # si le nombre de blocs est inférieur au nombre maximum de blocs à l'écran
            p_w = random.randint(100, 150) # largeur du bloc entre 100 et 150 pixels
            p_x = random.randint(0, ecran_width - p_w) # position du bloc sur l'axe des x entre 0 et la largeur de l'écran moins la largeur du bloc
            p_y = bloc.rect.y - random.randint(80, 120) # position du bloc sur l'axe des y par rapport au bloc précédent entre 80 et 120 pixels plus haut
            p_type = random.randint(1, 2) # type de bloc entre 1 et 2
            if p_type == 1 and score > 400: # si le type de bloc est 1 et que le score est supérieur à 400
                p_moving = True # le bloc est mobile
            else: # si le type de bloc est 2
                p_moving = False # le bloc est immobile
            bloc = Bloc(p_x, p_y, p_w, p_moving) # créer un bloc avec les paramètres définis
            bloc_group.add(bloc) # ajouter le bloc à la liste des blocs

        # mettre à jour les blocs
        bloc_group.update(scroll) # déplacer les blocs en fonction de la valeur de défilement de l'écran

        # réinitialiser le score
        if scroll > 0: # si la valeur de défilement de l'écran est supérieure à 0
            score += scroll # augmenter le score en fonction de la valeur de défilement de l'écran

        # affichage de la ligne du dernier meilleur score
        pygame.draw.line(ecran, white, (0, score - high_score + Scroll_thresh), (ecran_width, score - high_score + Scroll_thresh), 3)
        draw_text("MEILLEUR SCORE", font_small, black, ecran_width - 200, score - high_score + Scroll_thresh) # afficher le score du joueur

        # affichage les sprites
        bloc_group.draw(ecran) # afficher les blocs sur l'écran
        forrest.draw() # afficher le joueur

        # affichage du score
        draw_panel()

        # vérifier si le jeu est terminé
        if forrest.rect.top > ecran_height: # si le joueur sort de l'écran par le haut (mort)
            game_over = True # le jeu est terminé
            mort_fx.play() # jouer le son de mort
    else:
        if fade_counter < ecran_width: # si le rectangle noir n'a pas couvert l'écran
            fade_counter += 5 # augmenter la taille du rectangle noir
            for y in range(0, 6, 2): # parcourir la liste des valeurs de y
                pygame.draw.rect(ecran, black, (0, y * 100, fade_counter, 100)) # afficher le rectangle noir de la moitié supérieure de l'écran
                pygame.draw.rect(ecran, black, (ecran_width - fade_counter, (y + 1) * 100, ecran_width, 100)) # afficher le rectangle noir de la moitié inférieure de l'écran
        else :
            draw_text("TERMINÉ !", font_big, white, 170, 200) # afficher le texte TERMINÉ !
            draw_text("SCORE: " + str(score), font_big, white, 170, 250) # afficher le score du joueur
            draw_text("Appuyez sur espace pour rejouer", font_big, white, 60, 300) # afficher le texte pour rejouer
            if score > high_score: # si le score est supérieur au meilleur score
                high_score = score # le meilleur score devient le score du joueur
                with open("score.txt", "w") as file: # ouvrir le fichier score.txt en écriture
                    file.write(str(high_score)) # écrire le meilleur score dans le fichier
            key = pygame.key.get_pressed() # récupérer les touches du clavier appuyées
            if key[pygame.K_SPACE]: # si la touche espace est enfoncée
                game_over = False # réinitialiser le jeu
                score = 0 # réinitialiser le score
                scroll = 0 # réinitialiser le défilement de l'écran
                fade_counter = 0 # réinitialiser le rectangle noir
                forrest.rect.center = (ecran_width // 2, ecran_height - 150) # repositionnement de forrest
                bloc_group.empty() # réinitialiser les rochers
                bloc = Bloc(ecran_width // 2 -50, ecran_height - 100, 100, False) # créer les blocs de départ
                bloc_group.add(bloc) # ajouter les blocs de départ à la liste des blocs

    # gestion des événements
    for event in pygame.event.get(): # parcourir la liste des événements
        if event.type == pygame.QUIT: # si l'événement est de type QUIT
            if score > high_score: # si le score est supérieur au meilleur score
                high_score = score # le meilleur score devient le score du joueur
                with open("score.txt", "w") as file: # ouvrir le fichier score.txt en écriture
                    file.write(str(high_score)) # écrire le meilleur score dans le fichier
            run = False # quitter la boucle de jeu

    # mise à jour de l'écran
    pygame.display.update() 

pygame.quit()       