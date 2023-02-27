import time
import random
import pygame

# lite de mots
listeMot=["jeu", "constitutionnel", "joyaux", "temps", "plateforme", "typing", "visualisation", "huit", "labyrinthe", "courir", "manger", "vivre", "waterloo", "bowling", "choucroute", "noyau", "vouloir", "opter", "trois", "profiter", "hexagonal", "gicler", "satisfaire", "notice", "pompier", "statut", "victoire", "absolument", "noirceur", "cuisine", "fondre", "cycle", "dinosaure", "watt", "savoyard", "mariage", "jalousie", "heureusement", "satanique", "paradis", "jouer", "pamoison", "excentrique", "voyelle", "noyer", "choisir", "exulter", "pastorale", "voisin", "hongroise"]

# initialisation de pygame
pygame.init()

# création de la fenêtre et lui donner un titre
fenêtre = pygame.display.set_mode((800,600))
pygame.display.set_caption("TypingGump")

# chargement de l'image de fond et redimensionnement
fond = pygame.image.load("img/ville.jpeg").convert_alpha()
fond = pygame.transform.scale(fond,(800,600))

# choix de la police
maPolice=pygame.font.SysFont("Comic sans MS",35)

# variables
vitesse = 0.4
score=0
gamenotover=True
gamestarted=False

# fonction pour générer un mot aléatoire
def genererMot():
    global motActuel, motJoueur,x,y,vitesse
    # coordonnée x du mot aléatoire 
    x=random.randint(150,550)
    # coordonnée y
    y=150

    # augmentation de la vitesse du mot
    vitesse = vitesse + 0.05
    # mot aléatoire choisi dans la liste de mots
    motJoueur= ''

    # mot aléatoire choisi dans la liste de mots
    motActuel = random.choice(listeMot)

# appel de la fonction pour générer un mot aléatoire
genererMot()


# fonction pour afficher le texte
def montreTexte(x,y,text,sz):
    # choix de la police
    maPolice=pygame.font.SysFont("Comic sans MS",sz)
    # rendu du texte
    montexte = maPolice.render(text,True,(0,0,0))
    # affichage du texte
    fenêtre.blit(montexte,(x,y))

# initialisation de l'affichage de la fenêtre
def displayEcran():
    # affichage de l'image de fond
    fenêtre.blit(fond,(0,0))
    # si le jeu n'est pas terminé
    if gamenotover is False: 
        # affichage du texte "Game Over"
        montreTexte(100,200,"Le jeu est fini!!!",80)
        # affichage du score
        montreTexte(100,300,"Score: "+str(score),50)
    # si le jeu n'a pas encore commencé
    else:
        montreTexte(60,200,"Appuyer sur une touche pour commencer",36)
    # mise à jour de l'affichage
    pygame.display.flip()

    # initialisation de la variable attendre
    attendre=True
    while attendre:
        # parcours de la liste des événements
        for event in pygame.event.get():
            # si l'utilisateur quitte
            if event.type == pygame.QUIT:
                # on quitte pygame
                pygame.quit()
            # si aucune autre touche n'est appuyée
            if event.type== pygame.KEYDOWN:
                # 
                attendre = False

# loupe infinie jusqu'à ce que l'utilisateur quitte
while True:
    if gamenotover:
        if not gamestarted:
            # initialisation de l'affichage de la fenêtre
            displayEcran()
        # réglage de gamestarted à True
        gamestarted=True
    gamenotover=False

    # chargement de l'image du personnage et redimensionnement
    personnage = pygame.image.load("img/forrest.png").convert_alpha()
    personnage = pygame.transform.scale(personnage,(50,50))

    # affichage de l'image de fond 
    fenêtre.blit(fond,(0,0))

    y+=vitesse
    # affichage du personnage
    fenêtre.blit(personnage,(x-100,y))

    # affichage du mot actuel
    montreTexte(x,y,str(motActuel),35)
    # affichage du score
    montreTexte(300,5,'Score: '+str(score),35)

    # parcours de la liste des événements
    for event in pygame.event.get():
         # si l'utilisateur quitte
        if event.type == pygame.QUIT:
            # on quitte pygame
            pygame.quit()
            quit()
        # si le joueur appuie sur une autre touche
        elif event.type == pygame.KEYDOWN:
            # ajout d'une lettre au mot du joueur
            print(pygame.key.name(event.key))
            motJoueur+= pygame.key.name(event.key)
            # vérification de l'orthographe du mot du joueur
            if motActuel.startswith(motJoueur):
                # si le mot du joueur est égal au mot actuel
                if motActuel == motJoueur:
                    # augmentation du score
                    score += 10
                    # appel de la fonction pour générer un nouveau mot aléatoire
                    genererMot()
            # si le mot du joueur n'est pas égal au mot actuel
            else:
                displayEcran()
                time.sleep(2)
                pygame.quit()

    # si le mot n'est pas encore arrivé au bas de l'écran 
    if y< 590:
        pygame.display.update()
    # si le mot est arrivé au bas de l'écran
    else:
        displayEcran()            