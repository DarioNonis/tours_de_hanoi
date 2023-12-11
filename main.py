from turtle import *
from random import shuffle
import copy, time

def init(n):                                                            # On crée un plateau de jeu initial avec n disques sur le premier tour
    tour_de_depart = []
    for i in range(n, 0, -1):
        tour_de_depart.append(i)
    return [tour_de_depart, [], []]

def nbDisques(plateau, numtour):
    return len(plateau[numtour])                                        # Retourne le nombre de disques sur une tour donnée

def disqueSup(plateau, numtour):                                        
    if 0 <= numtour <= 2 and len(plateau[numtour]) != 0:
        return plateau[numtour][-1]                                     # On renvoie le numéro du disque supérieur (c'est-à-dire le plus grand) de la tour indiquée,
    return -1                                                           # sinon on renvoie -1 comme demandé dans l'énoncé

def posDisque(plateau, numdisque):                                      
    for tour in plateau:
        for disque in tour:
            if disque == numdisque:
                return tour                                             # Pour un dique donné, on renvoie la tour sur laquelle il se trouve
            
def verifDepl(plateau, nt1, nt2):
    autorise = False
    if disqueSup(plateau, nt1) < disqueSup(plateau, nt2) or disqueSup(plateau, nt2) == -1:
        autorise = True
    return autorise

def verifVictoire(plateau, n):
    liste_valide = []
    for i in range(n, 0, -1):
        liste_valide.append(i)
    if liste_valide == plateau[2]:                                      # On vérifie si la liste valide correspond à la configuration de la tour de droite
        return True
    return False

plateau_ord_org = (-300, -200)          # Coordonnées à l'origine de la base du plateau (coin supérieur gauche)
speed(0)
ht()
liste_coord_tours = []
title("Tours de Hanoï")
liste_couleurs = liste_couleurs = ["gold", "orange red", "cornflower blue", "dark khaki", "lavender", "lime green", "light salmon", "slate blue", "chocolate", "hot pink", "dark turquoise", "violet", "medium purple", "deep sky blue"]
shuffle(liste_couleurs)

def rectangle(x, y, longueur, largeur, couleur_contour="black", couleur_interieur="white", numero=0):        # Départ du rectangle du coin supérieur gauche ! (puis traçage dans le sens horaire)
    up(); goto(plateau_ord_org[0] + x, plateau_ord_org[1] + y); down()
    color(couleur_contour)
    fillcolor(couleur_interieur)                                # On remplit le rectangle de blanc pour éviter de devoir
    begin_fill()                                                # effacer la tour qui se trouve derrière.
    tracer(0, 0)
    for i in range(2):
        forward(longueur)
        right(90)
        forward(largeur)
        right(90)
    end_fill()
    if numero != 0:
        up(); goto(plateau_ord_org[0] + x + longueur / 2 - 4, plateau_ord_org[1] + y - largeur); down()
        write(numero, font=("Verdana", 13, "normal"))
    update()

def dessinePlateau(n):
    # On dessine la base
    rectangle(0, 0, 80 + 3*(40 + (n-1)*30), 20, couleur_interieur="lightgrey")     # La longueur est déterminée en fonction de n disques
    
    # On dessine les tours
    x = 37 + (n-1)*15                               # Le 37 ici sert juste à centrer la tour (qui est de largeur 6) 
    y = (n+1)*20                                    # Rappel : les coordonnées ont pour origine le coin supérieur gauche de la base (qui a pour coordonnées (0, 0))
    largeur = 6
    longueur = (n+1)*20
    liste_coord_tours.append((x, y))
    for i in range(3):
        rectangle(x, y, largeur, longueur)
        x += 30 + n*30
        liste_coord_tours.append((x, y))

def dessineDisque(nd, plateau, n):
    global liste_couleurs
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] == nd:
                x = 20 + i*(40 + (n-1)*30 + 20) + (n-nd)*15     
                y = 20 + j*20                                   
                longueur = 40 + (nd-1)*30                       
                largeur = 20                                    # La largeur est constante et de valeur 20.
                # print((n-1), len(liste_couleurs))
                rectangle(x, y, longueur, largeur, numero=nd, couleur_interieur=liste_couleurs[(nd-1) % len(liste_couleurs)])

def effaceDisque(nd, plateau, n):
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] == nd:
                # Calcul des coordonnées et de la longueur
                x = plateau_ord_org[0] + 20 + i*(40 + (n-1)*30 + 20) + (n-nd)*15
                y = plateau_ord_org[1] + 20 + j*20
                longueur = 40 + (nd-1)*30
                largeur = 20

                # On efface le disque
                color("white")
                fillcolor("white")
                begin_fill()
                up(); goto(x, y - (largeur-1)); down()
                goto(x, y)
                goto(x + longueur, y)
                goto(x + longueur, y - (largeur-1))
                goto(x, y - (largeur-1))
                end_fill()

                # On redessine la tour
                hauteur_tour = 20 + (n-nbDisques(plateau, i)+1)*20
                pos_tour_x, pos_tour_y = liste_coord_tours[i]
                rectangle(pos_tour_x, pos_tour_y, 6, hauteur_tour)
                
def dessineConfig(plateau, n):
    for i in range(n+1):
        dessineDisque(i, plateau, n)

def effaceTout(plateau, n):
    for i in range(n+1):
        effaceDisque(i, plateau, n)

        for tour in plateau:                        # On oublie pas de supprimer le disque i de son emplacement dans la configuration du plateau
            tour.remove(i) if i in tour else tour

def demandeNbDisques():
    nbdisques = 0
    while nbdisques < 1:
        try:
            nbdisques = int(input("\nCombien de disques souhaitez-vous ? : "))
            if nbdisques < 1:
                print("\033[1;91mVeuillez entrer un nombre entier supérieur ou égal à 1 !\033[0m")
        except:
            print("\033[1;91mVeuillez entrer une valeur correcte (nombre entier supérieur ou égal à 1) !\033[0m")
    return nbdisques

def lireCoords(plateau):
    # On demande d'abord la tour de départ, tout en vérifiant qu'un déplacemement de disque depuis celle-ci est possible :
    deplacement_possible = False
    while not deplacement_possible:
        
        tour_depart = ""
        try:
            while tour_depart not in [0, 1, 2] and tour_depart == "":               # On vérifie que le numéro donné soit 0, 1 ou 2,
                tour_depart = int(input("Quelle tour de départ \033[90m(0, 1 ou 2, -1 pour abandon, 3 pour annuler le coup précédent)\033[0m ? "))

                if tour_depart == -1:                                               # (Gestion du cas si abandon du joueur.)
                    return (tour_depart, None)
                
                if tour_depart == 3:
                    return (tour_depart, None)
                
                if tour_depart in [0, 1, 2]:
                    while plateau[tour_depart] == []:                               # et que la tour choisie ne soit pas vide.
                        tour_depart = int(input("\033[1;91mTour vide !\033[0m Quelle tour de départ \033[90m(0, 1 ou 2)\033[0m ? "))
                else:
                    print("\033[1;91mNuméro de tour invalide !\033[0m")
        
            liste_indice_tours = [0, 1, 2]
            liste_indice_tours.remove(tour_depart)

            if verifDepl(plateau, tour_depart, liste_indice_tours[0]) or verifDepl(plateau, tour_depart, liste_indice_tours[1]):    # Important : on vérifie qu'au moins un déplacement est possible,
                deplacement_possible = True                                                                                         # sinon on peut softlock le jeu
            else:
                print("\033[1;91mAucun déplacement possible depuis cette tour !\033[0m Veuillez en choisir une autre.")
            
        except:
            print("\033[1;91mVeuillez entrer une valeur correcte !\033[0m \033[90m(nombre entier égal à 0, 1 ou 2, -1 pour abandon)\033[0m")
    
    # Ensuite on demande la tour d'arrivée, tout en vérifiant qu'elle soit vide ou que son disque supérieur soit inférieur au disque supérieur de la tour de départ choisie
    tour_arrivee = ""
    while tour_arrivee == "":
        try:
            while tour_arrivee not in [0, 1, 2]:                                                                                            # Comme pour la tour de départ, on vérifie que le numéro donné soit 0, 1 ou 2
                tour_arrivee = int(input("Quelle tour d'arrivée \033[90m(0, 1 ou 2)\033[0m ? "))
                if tour_arrivee in [0, 1, 2] and disqueSup(plateau, tour_arrivee) != -1:                                                    # Si c'est le cas et si la tour contient un disque,
                    while disqueSup(plateau, tour_arrivee) < disqueSup(plateau, tour_depart) and disqueSup(plateau, tour_arrivee) != -1:    # on vérifie que celui-ci soit plus grand que le disque déplacé
                        tour_arrivee = int(input("\033[1;91mDéplacement interdit !\033[0m Quelle tour d'arrivée \033[90m(0, 1 ou 2)\033[0m ? "))
                elif tour_arrivee not in [0, 1, 2]:
                    print("\033[1;91mNuméro de tour invalide !\033[0m")
        except:
            print("\033[1;91mVeuillez entrer une valeur correcte !\033[0m \033[90m(nombre entier égal à 0, 1 ou 2)\033[0m")

    # Il ne reste plus qu'à vérifier si le numéro de la tour de départ est bien différent de la tour d'arrivée
    while tour_arrivee == tour_depart:
        print("\033[1;91mVotre tour d'arrivée ne peut pas être la même que la tour de départ !\033[0m")
        tour_arrivee = -1                                                                   # Si c'est le cas on redemande le numéro de la tour d'arrivée
        while tour_arrivee not in [0, 1, 2]:                                                # (On aurait pu faire une fonction pour éviter de répéter du code)
            tour_arrivee = int(input("Quelle tour d'arrivée \033[90m(0, 1 ou 2)\033[0m ? "))
            if tour_arrivee in [0, 1, 2] and disqueSup(plateau, tour_arrivee) != -1:
                while disqueSup(plateau, tour_arrivee) < disqueSup(plateau, tour_depart) and disqueSup(plateau, tour_arrivee) != -1:
                    tour_arrivee = int(input("\033[1;91mDéplacement interdit !\033[0m Quelle tour d'arrivée \033[90m(0, 1 ou 2)\033[0m ? "))
        
    return (tour_depart, tour_arrivee)

def jouerUnCoup(plateau, n):
    reflexion_start = time.time()
    deplacement = lireCoords(plateau)
    temps_de_reflexion = time.time() - reflexion_start
    disque_a_deplacer = disqueSup(plateau, deplacement[0])

    if deplacement[0] != -1 and deplacement[0] != 3:
        effaceDisque(disque_a_deplacer, plateau, n)
        for tour in plateau:
            tour.remove(disque_a_deplacer) if disque_a_deplacer in tour else tour
        plateau[deplacement[1]].append(disque_a_deplacer)

        dessineDisque(disque_a_deplacer, plateau, n)
    return (deplacement[0], temps_de_reflexion)

def boucleJeu(plateau, n):
    dico_coups = {}
    dico_coups[0] = copy.deepcopy(plateau)

    abandon = False
    coups_max = 2**n - 1                                                                 # On met le nombre de coups maximal au nombre de coup minimal possible
    nb_coup = 0
    liste_temps_reflexion = []

    while not verifVictoire(plateau, n) and not abandon and coups_max + n >= nb_coup:    # Boucle principale du jeu, on laisse une marge d'erreur de n coups possibles en plus au joueur
        print(f"\n\033[4;36mCoup numéro {nb_coup + 1}\033[0m\033[36m :\033[0m")

        debut_temps_reflexion = time.time()
        deplacement_reflexion = jouerUnCoup(plateau, n)
        choix_depart = deplacement_reflexion[0]
        liste_temps_reflexion.append(round(deplacement_reflexion[1], 1))

        if choix_depart == - 1:
            abandon = True

        elif choix_depart == 3:
            if len(dico_coups) > 1:                                         # Si au moins un coup a été joué,
                dico_coups = annulerDernierCoup(plateau, n, dico_coups)     # on annule le dernier coup et on modifie le dictionnaire des coups
                nb_coup -= 2                                                # on enlève 2 au nombre de coups pour en rajouter un par la suite donc au final décrémenter le compteur de 1
            else:
                print("\033[1;91mImpossible d'annuler le dernier coup si aucun coup n'a été joué !\033[0m")
                nb_coup -= 1                                                # On décrémente de 1 pour ne pas augumenter au final le nombre de tours

        nb_coup += 1
        dico_coups[nb_coup] = copy.deepcopy(plateau)                        # On rajoute le numéro de coups comme une clé du dictionnaire et on lui adresse la configuration du plateau comme valeur

    return (abandon, verifVictoire(plateau, n), nb_coup, coups_max, liste_temps_reflexion)

def dernierCoup(dico_coups):
    dernier_coup = len(dico_coups) - 1
    tour_depart, tour_arrivee = None, None

    dernier_coup_precedent = dico_coups[dernier_coup - 1]
    dernier_coup_actuel = dico_coups[dernier_coup]

    for i in range(3):
        if len(dernier_coup_precedent[i]) < len(dernier_coup_actuel[i]):        # On vérifie si la pile sur le tour i a diminué
            tour_arrivee = i
        elif len(dernier_coup_precedent[i]) > len(dernier_coup_actuel[i]):      # On vérifie si la pile sur le tour i a augmenté
            tour_depart = i

    return (tour_depart, tour_arrivee)

def annulerDernierCoup(plateau, n, dico_coups):
    # (basicalement le même code que dans jouerUnCoup)
    dernier_coup = dernierCoup(dico_coups)                                      # On récupère le dernier coup joué,
    disque_a_replacer = disqueSup(plateau, dernier_coup[1])                     # et le disque qui a été déplacé au dernier coup.
    effaceDisque(disque_a_replacer, plateau, n)                                 # Puis on fait l'opération inverse : on efface le disque sur l'interface Turtle.
    for tour in plateau:                                                        # On le supprime de la tour où il est,
        tour.remove(disque_a_replacer) if disque_a_replacer in tour else tour
    plateau[dernier_coup[0]].append(disque_a_replacer)                          # pour le replacer au bon endroit dans la tour où il était avant.

    dessineDisque(disque_a_replacer, plateau, n)        # On le redessine au bon endroit sur l'interface turtle,
    dico_coups.pop(len(dico_coups) - 1)                 # puis on efface le dernier coup du dictionnaire des coups

    return dico_coups

def sauvScore(dico_score, id_partie, nom, nd, nb_coups, temps_de_jeu, liste_temps_reflexion):          # Effet de bord sur dico_scores pour ajouter la partie gagnée
    dico_score[id_partie] = (nom, nd, nb_coups, temps_de_jeu, liste_temps_reflexion)

def afficheScores(dico_scores, liste_nbdisques_joues):
    # On affiche pour chaque numéro de nombre de disques joués, le score des parties qui ont étés jouées avec ce numéro
    for nd in liste_nbdisques_joues:

        # On créé une liste des différents scores pour pouvoir faire un tri ensuite
        tableau_scores = []
        for partie in dico_scores.keys():
            if dico_scores[partie][1] == nd:
                tableau_scores.append(dico_scores[partie])
        
        # On fait un tri (ici un tri bulle) sur tableau_scores,
        for i in range(len(tableau_scores)):
            for j in range(0, len(tableau_scores)-1-i):

                # qui trie par le nombre de coups,
                if tableau_scores[j][2] > tableau_scores[j + 1][2]:
                    tableau_scores[j], tableau_scores[j + 1] = tableau_scores[j + 1], tableau_scores[j]

                # ET par le temps de la partie (plus bas = meilleur).
                elif tableau_scores[j][2] == tableau_scores[j + 1][2] and tableau_scores[j][3] > tableau_scores[j + 1][3]:
                    tableau_scores[j], tableau_scores[j + 1] = tableau_scores[j + 1], tableau_scores[j]

        # Il ne reste plus qu'à parcourir la liste des différents scores triés
        print(f"\n\033[4;33mTableau des scores pour {nd} disques\033[0m\033[33m :\033[0m")
        i = 1
        for score in tableau_scores:
            nb = str(i) + "er " if i == 1 else str(i) + "ème"
            print(f"{nb} : {score[0]}, avec {score[2]} coups et {score[3]} secondes.")
            i += 1

def afficheChronos(dico_scores):    # Même fonction que afficheScores mais on trie seulement en fonction du temps (comme demandé dans le PDF)
    tableau_scores = []
    for partie in dico_scores.keys():
        tableau_scores.append(dico_scores[partie])
    
    # Tri seulement par le temps
    for i in range(len(tableau_scores)):
        for j in range(0, len(tableau_scores)-1-i):
            if tableau_scores[j][3] > tableau_scores[j + 1][3]:
                tableau_scores[j], tableau_scores[j + 1] = tableau_scores[j + 1], tableau_scores[j]

    # Affichage du tableau des scores triés
    if tableau_scores:
        print("\n\033[4;33mTableau des scores en fonction du temps\033[0m\033[33m :\033[0m")
        i = 1
        for score in tableau_scores:
            nb = str(i) + "er " if i == 1 else str(i) + "ème"
            print(f"{nb} : {score[0]}, avec {score[3]} secondes.")
            i += 1

def reflexionMoy(dico_scores):
    # On commence par créer un dictionnaire avec pour clés les noms des joueurs et pour valeurs des clés les temps de réflexion de chaque partie jouée par le joueur
    temps_reflexion_joueurs = {}
    for partie in dico_scores:
        liste_temps = dico_scores[partie][4].copy()
        if dico_scores[partie][0] not in temps_reflexion_joueurs:                 # On regarde si on a déjà ajouté une partie du joueur au temps_reflexion_joueurs
            temps_reflexion_joueurs[dico_scores[partie][0]] = liste_temps         # et on l'ajoute dans le temps_reflexion_joueurs si ce n'est pas le cas
        else:
            temps_reflexion_joueurs[dico_scores[partie][0]] += liste_temps        # sinon on concatène la liste du temps des parties jouées par ce joueur
    
    # Ensuite on fait un parcours simple du dictionnaire créé en affichant la moyenne des différents temps de réflexion
    reflexion_moyenne_joueurs = {}
    for joueur in temps_reflexion_joueurs:
        somme_temps = 0
        for temps_de_reflexion in temps_reflexion_joueurs[joueur]:
            somme_temps += temps_de_reflexion
        reflexion_moyenne_joueurs[joueur] = round(somme_temps / len(temps_reflexion_joueurs[joueur]), 1)
    
    return reflexion_moyenne_joueurs

def afficheRapide(reflexion_moyenne_joueur):
    # On crée un liste contenant les coupes (nom du joueur, temps de réflexion moyen) pour ensuite trier la liste (on ne peut pas trier un dictionnaire)
    liste_reflexion_joueurs = []
    for joueur in reflexion_moyenne_joueur:
        liste_reflexion_joueurs.append((joueur, reflexion_moyenne_joueur[joueur]))
    
    # On trie donc par la suite la liste des couples (nom du joueur, temps de réflexion moyen) que l'on vient de générer
    for i in range(len(liste_reflexion_joueurs)):
        for j in range(0, len(liste_reflexion_joueurs)-1-i):
            if liste_reflexion_joueurs[j][1] > liste_reflexion_joueurs[j + 1][1]:
                liste_reflexion_joueurs[j], liste_reflexion_joueurs[j + 1] = liste_reflexion_joueurs[j + 1], liste_reflexion_joueurs[j]
    
    if liste_reflexion_joueurs:
        print("\n\033[4;33mTableau des scores en fonction de leur rapidité de réflexion\033[0m\033[33m :\033[0m")
        i = 1
        for joueur in liste_reflexion_joueurs:
            nb = str(i) + "er " if i == 1 else str(i) + "ème"
            print(f"{nb} : {joueur[0]}, avec {joueur[1]} secondes de réflexion en moyenne.")
            i += 1

def solutionDeplacements(nbdisques, tour_depart=0, tour_milieu=1, tour_arrivee=2, l_d=[]):
    liste_deplacements = l_d
    if nbdisques > 0:
        solutionDeplacements(nbdisques - 1, tour_depart, tour_arrivee, tour_milieu, l_d)      # On va déplacer n-1 disques de la tour de départ à la tour du milieu
        liste_deplacements.append((tour_depart, tour_arrivee))                                # puis ajouter le déplacement du disque restant de la tour de départ à la tour d'arrivée
        solutionDeplacements(nbdisques - 1, tour_milieu, tour_depart, tour_arrivee, l_d)      # enfin, on déplace les n-1 disques de la tour du milieu à la tour d'arrivée
    return liste_deplacements

def resolutionAutomatique(plateau, n, liste_deplacements):
    for deplacement in liste_deplacements:
        disque_a_deplacer = disqueSup(plateau, deplacement[0])                                # On récupère le disque à déplacer de la tour de départ
        effaceDisque(disque_a_deplacer, plateau, n)                                           # Ne pas oublier d'effacer le disque du plateau
        
        for tour in plateau:
            tour.remove(disque_a_deplacer) if disque_a_deplacer in tour else tour             # On retire le disque de la tour de départ et on l'ajoute à la tour d'arrivée,
        plateau[deplacement[1]].append(disque_a_deplacer)

        dessineDisque(disque_a_deplacer, plateau, n)                                          # et pour finir, on dessine le nouvel emplacement du disque sur le plateau

        time.sleep(0.333)                                                                     # On ralentit l'exécution pour avoir le temps de voir les déplacements

# PROGRAMME PRINCIPAL

# Logo ASCII
print("\033[1;31m  _____                          _        _   _                 _   _ ")
print("\033[1;33m |_   _|__  _   _ _ __ ___    __| | ___  | | | | __ _ _ __   __(_)_(_)")
print("\033[1;31m   | |/ _ \\| | | | '__/ __|  / _` |/ _ \\ | |_| |/ _` | '_ \\ / _ \\| |  ")
print("\033[1;33m   | | (_) | |_| | |  \\__ \\ | (_| |  __/ |  _  | (_| | | | | (_) | |  ")
print("\033[1;31m   |_|\\___/ \\__,_|_|  |___/  \\__,_|\\___| |_| |_|\\__,_|_| |_|\\___/|_|  \033[0m")

dico_scores = {}
id_partie = 1
liste_nbdisques_joues = []

jouer = True
while jouer:

    print("""\n\033[4;33mMenu principal, que voulez vous faire\033[0m\033[33m ?\033[0m
            
\033[1;1m1:\033[0m Jouer
\033[1;1m2:\033[0m Affichage des scores (en fonction du nombre de disques)
\033[1;1m3:\033[0m Affichage des scores en fonction du temps de jeu
\033[1;1m4:\033[0m Affichage du score en fonction du temps de réflexion moyen
\033[1;1m5:\033[0m Résoudre automatiquement 
\033[1;1m6:\033[0m Quitter le jeu""")

    # On demande son choix (tout en gérant les potentielles erreurs)
    choix = 0
    while choix not in [1, 2, 3, 4, 5, 6]:
        try:
            choix = int(input("\nVotre choix \033[90m(1, 2, 3, 4, 5 ou 6)\033[0m ? "))
            if choix not in [1, 2, 3, 4, 5, 6]:
                print("\033[1;91mVeuillez entrer un numéro de choix correct !\033[0m \033[90m(1, 2, 3, 4, 5 ou 6)\033[0m")
        except:
            print("\033[1;91mVeuillez entrer numéro de choix correct !\033[0m \033[90m(1, 2, 3, 4, 5 ou 6)\033[0m")
        
    if choix == 6:
        jouer = False
        # choix = 1               # Pour sortir de la boucle
        print("\033[30mAu revoir !\033[0m")

    elif choix == 2:
        afficheScores(dico_scores, liste_nbdisques_joues)
        choix = 0                 # (Permet de sortir de la boucle du menu principal)

    elif choix == 3:
        afficheChronos(dico_scores)
        choix = 0

    elif choix == 4:
        afficheRapide(reflexionMoy(dico_scores))
        choix = 0

    elif choix == 5:
        # On initialise juste ce qu'il faut pour que le programme puisse résoudre le problème (notamment le plateau turtle)
        liste_coord_tours = []
        nbdisques = demandeNbDisques()
        plateau = init(nbdisques); dessinePlateau(nbdisques); dessineConfig(plateau, nbdisques)
        
        input("\033[90mPressez la touche entrée pour résoudre le problème automatiquement.\033[0m")
        resolutionAutomatique(plateau, nbdisques, solutionDeplacements(nbdisques, l_d=[]))
        input("\033[90mPressez la touche entrée pour quitter.\033[0m")
        
        # On efface les dessins dans l'interface turtle et on sort de la boucle
        clearscreen(); speed(0); ht()
        choix = 0

    elif choix == 1:
        liste_coord_tours = []      # On vide la liste des coordonnées des tours pour éviter des bugs graphiques si jamais on change de nombre de disques à la prochaine partie

        # On demande à l'utilisateur un nombre de disques supérieur ou égal à 2
        nbdisques = demandeNbDisques()

        start_time = time.time()

        # Initialisation du plateau et des disques dans l'interface de turtle
        plateau = init(nbdisques)
        dessinePlateau(nbdisques)
        dessineConfig(plateau, nbdisques)

        # Démarrage du jeu puis récupération des résultats une fois terminé
        resultat = boucleJeu(plateau, nbdisques)
        temps_de_jeu = time.time() - start_time

        if resultat[0]:                                                     # Cas de l'abandon
            print(f"\n\033[33mAbandon de la partie\033[0m après {resultat[2] - 1} coup(s).")

        elif resultat[3] + nbdisques < resultat[2]:                         # Cas de la défaite
            print(f"\n\033[1;91mPerdu !\033[0m Vous avez fait trop de coups \033[90m(le maximum autorisé ici était {resultat[3] + nbdisques} coups).\033[0m")

        elif resultat[1]:                                                   # Cas de la victoire
            print(f"\n\033[1;92mVictoire !\033[0m Gagné en {resultat[2]} coups \033[90m(le minimum de coups possibles pour {nbdisques} disques étant {resultat[3]} coups)\033[0m.")
            nom = input("\nEntrez votre nom : ")
            sauvScore(dico_scores, id_partie, nom, nbdisques, resultat[2], round(temps_de_jeu, 1), resultat[4])
            
            # On ajoute dans la liste des numéros de disques joués le nombre de disques entré par l'utilisateur si ce nombre n'est pas déjà dans la liste
            if nbdisques not in liste_nbdisques_joues:
                liste_nbdisques_joues.append(nbdisques)
            
            # On incrémente l'id de la partie pour ne pas supprimer d'anciens scores
            id_partie += 1

        # On efface les dessins dans l'interface turtle et on sort de la boucle
        clearscreen(); speed(0); ht()
        choix = 0