#Importation des bibliothèques
import pygame
from random import randint
from sys import exit   # importe un module qui permet de quitter correctement l'application

#Initialisation de Pygame
pygame.init()

# initialise la fenetre
taille_fenetre = (800, 400)
fenetre = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Swimmy Fish")

clock = pygame.time.Clock()   # horloge qui permettra de limiter les images par seconde

################### Initialisation des ressources ####################
# initialisation de l'image du joueur et agrandissement
image_joueur = pygame.image.load("images/joueur.png").convert_alpha()     # charge l'image du joueur à partir du dossier "images"
image_joueur = pygame.transform.scale(image_joueur, (70, 65))   # agrandit l'image et lui définit une largeur de 70 pixels et une hauteur de 65 pixels

# initialisation des images des tuyaux
image_tuyau_bas = pygame.image.load("images/tuyau-bas.png").convert_alpha()   # convert alpha sert a considerablement ameliorer les performances
image_tuyau_bas = pygame.transform.scale(image_tuyau_bas, (110, 360))

image_tuyau_haut = pygame.image.load("images/tuyau-haut.png").convert_alpha()
image_tuyau_haut = pygame.transform.scale(image_tuyau_haut, (110, 360))

# initialisation du fond d'ecran
fond_ecran = pygame.image.load("images/fond-ecran.png").convert_alpha()
fond_ecran = pygame.transform.scale(fond_ecran, (800, 400))

image_titre = pygame.image.load("images/titre.png").convert_alpha()
image_titre = pygame.transform.scale(image_titre, (400, 200))

# initialisation du fond d'ecran de fin de jeu
fond_ecran_game_over = pygame.image.load("images/fond-ecran-game-over.png").convert_alpha()
fond_ecran_game_over = pygame.transform.scale(fond_ecran_game_over, (800, 400))

image_game_over = pygame.image.load("images/game-over.png").convert_alpha()
image_game_over = pygame.transform.scale(image_game_over, (400, 200))

image_joueur_mort = pygame.image.load("images/joueurM.png").convert_alpha()     # charge l'image du joueur à partir du dossier "images"
image_joueur_mort = pygame.transform.scale(image_joueur_mort, (70, 65))   # agrandit l'image et lui définit une largeur de 70 pixels et une hauteur de 65 pixels

# initialisation de la police d'ecriture des textes
police_ecriture = pygame.font.Font("Pixeled.ttf", 16)        # charge le fichier et lui définit une taille de 16

son_lancement = pygame.mixer.Sound("sons/son-lancement.ogg")   # charge le son de demarrage de la partie
son_score = pygame.mixer.Sound("sons/son-score.ogg")    # charge le son qui se jouera quand le joueur passe un tuyau
son_mort_bordures = pygame.mixer.Sound("sons/son-mort-bordures.ogg")  # charge le son qui se jouera quand le joueur dépassera les bordures
son_mort_tuyaux = pygame.mixer.Sound("sons/son-mort-tuyaux.ogg")  # charge le son qui se jouera quand le aura une collision avec un des tuyaux

################## creation des fonctions des tuyaux ##########################

# Pour rappel dans pygame un rectangle prend 4 arguments :
#   -Le premier à l'index 0 correspond à sa position x
#   -Le second à l'index 1 correspond à sa position y
#   -Le troisième à l'index 2 correspond à sa largeur
#   -Le quatrième à l'index 3 correspond à sa hauteur

def creer_tuyau_bas(position_x_creation_tuyaux):
    #generation du tuyau du bas
    position_y_tuyau_bas = randint(90, taille_fenetre[1]) #70 pour laisser au joueur l'espace de passer
    nouveau_tuyau_bas = pygame.Rect(position_x_creation_tuyaux, position_y_tuyau_bas, image_tuyau_bas.get_rect()[2], image_tuyau_bas.get_rect()[3])

    return nouveau_tuyau_bas

def creer_tuyau_haut(position_x_creation_tuyaux, position_y_tuyau_bas):
    #generation du tuyau du haut

    # dans cette fonction on prend en argument la position y du tuyau du bas pour generer le tuyau du haut 85 pixels au dessus 

    position_y_tuyau_haut = position_y_tuyau_bas - (85 + image_tuyau_bas.get_rect()[3]) # le tuyau du haut sera généré 80 pixels au dessus du tuyau du bas
    nouveau_tuyau_haut = pygame.Rect(position_x_creation_tuyaux, position_y_tuyau_haut, image_tuyau_haut.get_rect()[2], image_tuyau_haut.get_rect()[3])
    
    return nouveau_tuyau_haut


def collision_tuyaux(tuyau_bas, tuyau_haut, rectangle_joueur):

    if rectangle_joueur.colliderect(tuyau_bas):      # si le joueur rentre en collision avec le tuyau, return True qui persmettra de savoir qu'il y a bien une collision
        return True
    if rectangle_joueur.colliderect(tuyau_haut):
        return True


# Fonction qui verifie si le joueur a passé des tuyaux, si c'est le cas le score est incrémenté
def a_passe_tuyaux(vitesse_tuyaux, position_x_tuyaux):

    ### Verifie que la position est à une certaine position pour que le score soit incrémenté
    ### Ca varie selon la vitesse des tuyaux car ils ne passent pas forcement par un point en se déplacant
    ### Par example à un vitesse de trois, leur position x ne sera jamais de 150
    if vitesse_tuyaux == 2:
        if position_x_tuyaux == 150:
            return True
    elif vitesse_tuyaux == 3:
        if position_x_tuyaux == 149 or position_x_tuyaux == 151:
            return True
    elif vitesse_tuyaux == 4:
        if position_x_tuyaux == 152:
            return True

 ################################# Menus ################
#Boucle de jeu
def jeu(difficulte):

    ###################Initialisation des variables

    # initialisation de la variable joueur qui est un rectangle qui possede une position et un taille
    joueur = pygame.Rect(150, 100, image_joueur.get_rect()[2], image_joueur.get_rect()[3])
    vitesse_verticale_joueur = 2.25   ## vitesse verticale du joueur 2.25
    score_joueur = 0  # initialisation de la variable score de la partie

    # initialisation des variables tuyaux qui contiendrons les rectangles des tuyaux
    tuyau_bas = creer_tuyau_bas(1100)
    tuyau_haut = creer_tuyau_haut(1100, tuyau_bas[1])

    if difficulte == 'facile':
        vitesse_tuyaux = 2          # 2 = facile
    elif difficulte == 'moyen':
        vitesse_tuyaux = 3          # 3 = moyen
    elif difficulte == 'difficile':
        vitesse_tuyaux = 4          # 4 = difficile
    elif difficulte == 'par defaut':
        vitesse_tuyaux = 2    # par defaut sera 2 et augmentera progressivement en fonction du score

    particules = []  # liste qui contiendra les particules générés par le joueur

    # tout ce qui se trouve dans la boucle est éxecuté plusieurs fois par seconde
    running = True
    while running:
        
        clock.tick(120) # limite les images par seconde a 130   (ce qui fait que la boucle se repetera 130 fois par seconde)
        
        ############ Detection des évenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # desinitialise toute la librairie pygame
                exit()

        # detection des touches du clavier
        key = pygame.key.get_pressed()        # permet d'obtenir les touches cliquées par le joueur
        if key[pygame.K_ESCAPE]:   # si le joueur clique sur la touche echap du clavier, quitte le jeu
            pygame.quit()
            exit()

        if key[pygame.K_UP]:
            joueur[1] -= vitesse_verticale_joueur
        if key[pygame.K_DOWN]:
            joueur[1] += vitesse_verticale_joueur

        # Si le joueur dépasse les bordures basse ou haute, le joueur perd
        if joueur[1] >= taille_fenetre[1] - image_joueur.get_rect()[3]:
            son_mort_bordures.play()
            running = False
        if joueur[1] <= 0 - image_joueur.get_rect()[3]:
            son_mort_bordures.play()
            running = False

        ################# Actualisation des éléments

        if tuyau_bas[0] <= -110:      #-110 correspond a la largeur du tuyau, donc quand le tuyau est hors de l'ecran, il est supprimé

            # remplace les tuyaux passés hors de l'ecran vers la gauche par des nouveaux qui sont générés à droite
            tuyau_bas = creer_tuyau_bas(800)
            tuyau_haut = creer_tuyau_haut(800, tuyau_bas[1]) # on créé la position y du tuyau du haut à partir de celle du tuyau du bas
            
        tuyau_bas[0] -= vitesse_tuyaux    # fait avancer le tuyau du bas vers la gauche
        tuyau_haut[0] -= vitesse_tuyaux    # fait avancer le tuyau du haut vers la gauche

        #detecte si le joueur touche un tuyau, si c'est le cas la partie se termine
        if collision_tuyaux(tuyau_bas, tuyau_haut, joueur) == True:
            son_mort_tuyaux.play()
            running = False

        if(a_passe_tuyaux(vitesse_tuyaux, tuyau_bas[0]) == True):    # si le joueur passe les tuyaux, incrémente le score du joueur (on prend la position x du tuyau bas car sa position x est commune avec celle du haut)
            score_joueur += 1
            son_score.play()

        if difficulte == 'par defaut':
            # accelere la vitesse au bout d'un certain score
            if score_joueur >= 15 and tuyau_bas[0] < -80:          # -80 est la position a laquelle les tuyaux ne sont plus visibles sur l'ecran, à ce moment là la vitesse pourra etre modifiée
                vitesse_tuyaux = 4
            elif score_joueur >= 5 and tuyau_bas[0] < -80:
                vitesse_tuyaux = 3

        ####################### Affichage des éléments
        fenetre.blit(fond_ecran, (0,0))   # dessine le fond d'ecran a la position x = 0, y = 0

        ###### animation de particules
        position_x_particule = joueur[0]+70
        position_y_particule = randint(joueur[1]+15, joueur[1]+40)

        # créé une liste qui contient les caracteristiques de la future particule (qui est un cercle). elle contient une liste qui contient la position initiale (qui est par defaut celle du joueur) puis un integer qui sera le rayon du cercle
        # cette liste est ajoutée à la liste de particules.
        
        particules.append([[position_x_particule,position_y_particule], 2]) 
        for particule in particules:
            particule[0][0] -= randint(0, 3)  
            particule[0][1] -= randint(0, vitesse_tuyaux) # deplace la position y de la particule de facon aléatoire (entre 0 et la vitesse des tuyaux )

            pygame.draw.circle(fenetre, (0, 0, 200), particule[0], 2)

            if particule[0][0] <= 0:   #si la position x de la particule est en dessous de 0, elle est suprimmée
                particules.remove(particule)
            

        fenetre.blit(image_joueur, (joueur[0], joueur[1]))

        fenetre.blit(image_tuyau_bas, (tuyau_bas[0], tuyau_bas[1]))   # dessine l'image du tuyau de bas sur le rectangle du tuyau du bas
        fenetre.blit(image_tuyau_haut, (tuyau_haut[0], tuyau_haut[1]))

        texte_score = police_ecriture.render("Score : {0}".format(score_joueur), 2, (255, 255, 255)) ## 255 255 255 correspond à la couleur du texte
        fenetre.blit(texte_score, (300, 0))

        #actualisation des images affichées
        pygame.display.update()

    # quand la boucle se termine, la fonction jeu() renverra le score de la partie ainsi que la difficulte
    return {'score':score_joueur, 'difficulte':difficulte}


def menu_principal():

    particules = []
 
    difficulte_selectionne = 0  # difficulte en integer pour pouvoir decrementer ou incrementer 
    # 0 = progressif, 1 = facile, 2 = moyen, 3 = difficile

    pygame.mixer.music.load('sons/musique-menu-principal.ogg') # initialise la musique d'arriere plan du menu principal
    pygame.mixer.music.set_volume(0.7)    # regle le volume de la musique
    pygame.mixer.music.play(-1) # -1 fait que la musique se repete quand elle se termine, ce qui fait que la musique se joue en continu

    ## boucle du menu principal quand l'application se lance
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                
                pygame.mixer.music.stop()  # arrete la musique juste avant de quitter la fonction

                return difficulte_selectionne   #retourne la difficulté selectionnée

            if key[pygame.K_LEFT]:
                if difficulte_selectionne > 0:   # on fait cette verification pour pas que le joueur puisse selectionner une difficulte qui n'existe pas
                    difficulte_selectionne-=1
            if key[pygame.K_RIGHT]:
                if difficulte_selectionne < 3:   # 3 correspond a la difficule maximale
                    difficulte_selectionne+=1


        clock.tick(130) # limite les images par seconde a 130   (ce qui fait que la boucle se repetera 130 fois par seconde)
        fenetre.blit(fond_ecran, (0,0))  # 0 0 correspond a la position

        # animation particules, qui est similaire a celle qui a été créée dans la fonction jeu
        # on dessine l'animation devant le fond d'ecran et derriere l'image du titre pour qu'elle soit derriere le titre et visible (que le fond ne la cache pas)
        position_x_particule = pygame.mouse.get_pos()[0] # prend la position x de la souris
        position_y_particule = pygame.mouse.get_pos()[1]

        particules.append([[position_x_particule,position_y_particule], 3]) 
        
        for particule in particules:
            
            particule[0][0] -= randint(-4, 4) # deplace la particule soit vers la gauche (- sur l'axe x) soit vers la droite (car - et - font + sur l'axe x)
            particule[0][1] -= randint(1, 4) # déplace la particule vers le haut (position y)

            pygame.draw.circle(fenetre, (0, 0, 200), particule[0], particule[1])

            if particule[0][1] <= 0:   #si la position y de la particule est en dessous 0, elle est supprimée de la liste
                particules.remove(particule)

    
        fenetre.blit(image_titre, (200, 40))
        fenetre.blit((police_ecriture.render("Cliquez sur la touche Espace pour jouer", 2, (255,255, 255))), (150, 230))  # 255 255 255 est un code rgb en hexadecimal
        
        # affiche la difficulté selectionnée
        if difficulte_selectionne == 0:
            fenetre.blit((police_ecriture.render("Difficulté selectionnée : Par défaut", 2, (255,255, 255))), (150, 260))
        elif difficulte_selectionne == 1:
            fenetre.blit((police_ecriture.render("Difficulté selectionnée : Facile", 2, (255,255, 255))), (150, 260))
        elif difficulte_selectionne == 2:
            fenetre.blit((police_ecriture.render("Difficulté selectionnée : Moyen", 2, (255,255, 255))), (150, 260))
        elif difficulte_selectionne == 3:
            fenetre.blit((police_ecriture.render("Difficulté selectionnée : Difficile", 2, (255,255, 255))), (150, 260))

        pygame.display.update()

    


def game_over(meilleur_score):

    rectangle_joueur_mort = pygame.Rect(150, -100, image_joueur.get_rect()[2], image_joueur.get_rect()[3])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                return True
            if key[pygame.K_ESCAPE]:
                return False

        fenetre.blit(fond_ecran_game_over, (0,0))

        ############# animation du joueur qui meurt
        clock.tick(400)
        if rectangle_joueur_mort[1] < 370:    # 370 est la position a laquelle le joueur arrete de tomber
            rectangle_joueur_mort[1] += 1
        fenetre.blit(image_joueur_mort, (rectangle_joueur_mort[0], rectangle_joueur_mort[1]))

        fenetre.blit(image_game_over, (210, 40))
        fenetre.blit((police_ecriture.render("Cliquez sur Espace pour rejouer", 2, (255,255,255))), (200, 220))

        texte_score = police_ecriture.render("Votre meilleur score est de : {}".format(meilleur_score['score']), 2, (255, 255, 255))
        fenetre.blit(texte_score, (200, 250))

        texte_difficulte = police_ecriture.render("en difficulte {}".format(meilleur_score['difficulte']), 2, (255, 255, 255))
        fenetre.blit(texte_difficulte, (200, 280))

        pygame.display.update()


menu_selectionne = 'menu_principal'  # variable qui montre le menu selectionné
meilleur_score = {'score': 1, 'difficulte': 'par defaut'}              # initialise la variable  de type dictionnaire qui contient le score du joueur et la difficultz a laquelle elle a été atteinte
difficulte = 'par defaut'         # difficulte est une chaine de caractere pour pouvoir etre affiché avec la police d'ecriture
# la difficulte peut etre selectionnée avec les fleches directionnelles

# boucle qui ne se termine jamais et qui verifie à chaque fois le menu qui est en cours
# elle execute aussi les fonctions tels que le jeu
while True:
    if menu_selectionne == 'menu_principal':
        difficulte_selectionne = menu_principal()

        if difficulte_selectionne == 1:
            difficulte = 'facile'
        elif difficulte_selectionne == 2:
            difficulte = 'moyen'
        elif difficulte_selectionne == 3:
            difficulte = 'difficile'
        else:
            difficulte = 'par defaut'

        son_lancement.play()     # joue le son du lancemant de partie
        menu_selectionne = 'menu_jeu'


    elif menu_selectionne == 'menu_jeu':
        score_partie = jeu(difficulte)     # comme le jeu retourne la valeur du score, on l'attribue à cette variable. Et execute aussi la fonction jeu()
        if meilleur_score['score'] < score_partie['score']:  #si le score de la partie est le meilleur, definit le meilleur score comme le score de la partie
            meilleur_score['score'] = score_partie['score']
            meilleur_score['difficulte'] = score_partie['difficulte']

        # si la difficulté de la partie precedente est differente du meilleur score, remplace le meilleur score par celui de la partie precedente
        if meilleur_score['difficulte'] != score_partie['difficulte']:  
            meilleur_score['score'] = score_partie['score']
            meilleur_score['difficulte'] = score_partie['difficulte']

        # quand la partie est terminée, la variable du menu sélectionné devient le menu de fin de partie
        menu_selectionne = 'game_over'


    elif menu_selectionne == 'game_over':
        rejouer = game_over(meilleur_score)

        if rejouer == True:
            son_lancement.play()
            menu_selectionne = "menu_jeu"
        elif rejouer == False:
            
            menu_selectionne = "menu_principal"