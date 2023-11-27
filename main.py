from turtle import *
import copy, time

def init(n):
    tour_de_depart = []
    for i in range(n, 0, -1):
        tour_de_depart.append(i)
    return [tour_de_depart, [], []]

def nbDisques(plateau, numtour):
    return len(plateau[numtour])

def disqueSup(plateau, numtour):
    if 0 <= numtour <= 2 and len(plateau[numtour]) != 0:
        return plateau[numtour][-1]
    return -1

def posDisque(plateau, numdisque):
    for tour in plateau:
        for disque in tour:
            if disque == numdisque:
                return tour
            
def verifDepl(plateau, nt1, nt2):
    autorise = False
    if disqueSup(plateau, nt1) < disqueSup(plateau, nt2) or disqueSup(plateau, nt2) == -1:
        autorise = True
    return autorise

def verifVictoire(plateau, n):
    liste_valide = []
    for i in range(n, 0, -1):
        liste_valide.append(i)
    if liste_valide == plateau[2]:
        return True
    return False

plateau_ord_org = (-300, -200)          # Coordonnées à l'origine de la base du plateau (coin supérieur gauche)
speed(4000)
liste_coord_tours = []
title("Tours de Hanoï")

def rectangle(x, y, longueur, largeur, couleur="black"):        # Départ du rectangle du coin supérieur gauche ! (puis traçage dans le sens horaire)
    up()
    goto(plateau_ord_org[0] + x, plateau_ord_org[1] + y)        # Coordonnées du point supérieur gauche
    down()
    color(couleur)
    fillcolor("white")                                          # On remplit le rectangle de blanc pour éviter de devoir
    begin_fill()                                                # effacer la tour qui se trouve derrière.
    for i in range(2):
        forward(longueur)
        right(90)
        forward(largeur)
        right(90)
    end_fill()

    # La boucle pourrait être remplacée par :

    # goto(plateau_ord_org[0] + x + longueur, plateau_ord_org[1] + y)
    # goto(plateau_ord_org[0] + x + longueur, plateau_ord_org[1] + y - largeur)
    # goto(plateau_ord_org[0] + x, plateau_ord_org[1] + y - largeur)
    # goto(plateau_ord_org[0] + x, plateau_ord_org[1] + y)

    # et ce serait UN PEU plus rapide

def dessinePlateau(n):
    # On dessine la base
    rectangle(0, 0, 80 + 3*(40 + (n-1)*30), 20)     # la longueur est déterminée en fonction de n disques
    
    # On dessine les tours
    x = 37 + (n-1)*15                               # le 37 ici sert juste à centrer la tour (qui est de largeur 6) 
    y = (n+1)*20                                    # Rappel : les coordonnées ont pour origine le coin supérieur gauche de la base (qui a pour coordonnées (0, 0))
    largeur = 6
    longueur = (n+1)*20
    liste_coord_tours.append((x, y))
    for i in range(3):
        rectangle(x, y, largeur, longueur)
        x += 30 + n*30
        liste_coord_tours.append((x, y))

def dessineDisque(nd, plateau, n):
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] == nd:
                x = 20 + i*(40 + (n-1)*30 + 20) + (n-nd)*15     # Oui le calcul des coordonnées du disque est horrible,
                y = 20 + j*20                                   # mais avec la puissance des math (et de mon énorme cerveau),
                longueur = 40 + (nd-1)*30                       # on fait des trucs absolument incroyables ! (bon ok j'ai mis 30mn à faire cte ptn de fonction)
                largeur = 20                                    # La largeur est constante et de valeur 20.
                rectangle(x, y, longueur, largeur)

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
                up(); goto(x, y - (largeur-1)); down()
                goto(x, y)
                goto(x + longueur, y)
                goto(x + longueur, y - (largeur))

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

def effacePlateauDisques(n):
    x = 0
    y = (n+1)*20
    longueur = 80 + 3*(40 + (n-1)*30)
    largeur = (n+2)*20
    rectangle(x, y, longueur, largeur, "white")

def lireCoords(plateau):
    # On demande d'abord la tour de départ, tout en vérifiant qu'un déplacemement de disque depuis celle-ci est possible:
    deplacement_possible = False
    while not deplacement_possible:
        
        tour_depart = ""
        try:
            while tour_depart not in [0, 1, 2] and tour_depart == "":                                                         # on vérifie que le numéro donné soit 0, 1 ou 2,
                tour_depart = int(input("Quelle tour de départ (0, 1 ou 2, -1 pour abandon, 3 pour annuler le coup précédent) ? "))

                if tour_depart == -1:               # (Gestion du cas si abandon du joueur.)
                    return (tour_depart, None)
                
                if tour_depart == 3:
                    return (tour_depart, None)
                
                if tour_depart in [0, 1, 2]:
                    while plateau[tour_depart] == []:                                                   # et que la tour choisie ne soit pas vide.
                        tour_depart = int(input("Tour vide ! Quelle tour de départ (0, 1 ou 2) ? "))
                else:
                    print("Numéro de tour invalide !")
        
            liste_indice_tours = [0, 1, 2]
            liste_indice_tours.remove(tour_depart)

            if verifDepl(plateau, tour_depart, liste_indice_tours[0]) or verifDepl(plateau, tour_depart, liste_indice_tours[1]):    # Important : on vérifie qu'au moins un déplacement est possible,
                deplacement_possible = True                                                                                         # sinon on peut softlock le jeu
            else:
                print("Aucun déplacement possible depuis cette tour ! Veuillez en choisir une autre.")
            
        except:
            print("Veuillez entrer une valeur correcte (nombre entier égal à 0, 1 ou 2, -1 pour abandon) !")
    
    # Ensuite on demande la tour d'arrivée, tout en vérifiant qu'elle soit vide ou que son disque supérieur soit inférieur au disque supérieur de la tour de départ choisie
    tour_arrivee = ""
    while tour_arrivee == "":
        try:
            while tour_arrivee not in [0, 1, 2]:                                                                                            # comme pour la tour de départ, on vérifie que le numéro donné soit 0, 1 ou 2
                tour_arrivee = int(input("Quelle tour d'arrivée (0, 1 ou 2) ? "))
                if tour_arrivee in [0, 1, 2] and disqueSup(plateau, tour_arrivee) != -1:                                                    # si c'est le cas et si la tour contient un disque,
                    while disqueSup(plateau, tour_arrivee) < disqueSup(plateau, tour_depart) and disqueSup(plateau, tour_arrivee) != -1:    # on vérifie que celui-ci soit plus grand que le disque déplacé
                        tour_arrivee = int(input("Déplacement interdit ! Quelle tour d'arrivée (0, 1 ou 2) ? "))
                elif tour_arrivee not in [0, 1, 2]:
                    print("Numéro de tour invalide !")
        except:
            print("Veuillez entrer une valeur correcte (nombre entier égal à 0, 1 ou 2) !")

    # Il ne reste plus qu'a vérifier si le numéro de la tour de départ est bien différent de la tour d'arrivée
    while tour_arrivee == tour_depart:
        print("Votre tour d'arrivée ne peut pas être la même que la tour de départ !")
        tour_arrivee = -1                                                                   # Si c'est le cas on redemande le numéro de la tour d'arrivée
        while tour_arrivee not in [0, 1, 2]:                                                # (Oui j'aurais pu faire une fonction pour éviter de répéter du code)
            tour_arrivee = int(input("Quelle tour d'arrivée (0, 1 ou 2) ? "))
            if tour_arrivee in [0, 1, 2] and disqueSup(plateau, tour_arrivee) != -1:
                while disqueSup(plateau, tour_arrivee) < disqueSup(plateau, tour_depart) and disqueSup(plateau, tour_arrivee) != -1:
                    tour_arrivee = int(input("Déplacement interdit ! Quelle tour d'arrivée (0, 1 ou 2) ? "))
        
    return (tour_depart, tour_arrivee)

def jouerUnCoup(plateau, n):
    deplacement = lireCoords(plateau)
    disque_a_deplacer = disqueSup(plateau, deplacement[0])
    
    if deplacement[0] != -1 and deplacement[0] != 3:
        effaceDisque(disque_a_deplacer, plateau, n)
        for tour in plateau:
            tour.remove(disque_a_deplacer) if disque_a_deplacer in tour else tour
        plateau[deplacement[1]].append(disque_a_deplacer)

        dessineDisque(disque_a_deplacer, plateau, n)
    return deplacement[0]

def boucleJeu(plateau, n):
    dico_coups = {}
    dico_coups[0] = copy.deepcopy(plateau)

    abandon = False
    coups_max = 2**n - 1                                                                # On met le nombre de coups maximal au nombre de coup minimal possible
    nb_coup = 0

    while not verifVictoire(plateau, n) and not abandon and coups_max + n >= nb_coup:    # Boucle principale du jeu, on laisse une marge d'erreur de n coups possible en plus au joueur
        print("\nCoup numéro", nb_coup + 1)
        choix_depart = jouerUnCoup(plateau, n)        

        if choix_depart == - 1:
            abandon = True

        elif choix_depart == 3:
            if len(dico_coups) > 1:                                         # Si au moins un coup a été joué,
                dico_coups = annulerDernierCoup(plateau, n, dico_coups)     # On annule le dernier coup et on modifie le dictionnaire des coups
                nb_coup -= 2                                                # On enlève 2 au nombre de coups pour en rajouter un par la suite donc au final décrémenter le compteur de 1
            else:
                print("Impossible d'annuler le dernier coup si aucun coup n'a été joué !")
                nb_coup -= 1                                                # On décrémente de 2 pour ne pas augumenter au final le nombre de tours

        nb_coup += 1
        print(nb_coup) # DEBUG
        dico_coups[nb_coup] = copy.deepcopy(plateau)                        # On rajoute le numéro de coups comme une clé du dictionnaire et on lui adresse la configuration du plateau comme valeur

    return (abandon, verifVictoire(plateau, n), nb_coup, coups_max)

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

    dessineDisque(disque_a_replacer, plateau, n)        # On le redessine au bon endroit sur l'interface tutrle,
    dico_coups.pop(len(dico_coups) - 1)                 # puis on efface le dernier coup du dictionnaire des coups

    return dico_coups

def sauvScore(dico_score, id_partie, nom, nd, nb_coups, temps_de_jeu):          # Effet de bord sur dico_scores pour ajouter la partie gagnée
    dico_score[id_partie] = (nom, nd, nb_coups, temps_de_jeu)

def afficheScores(dico_scores, nd):
    tableau_scores = []
    for partie in dico_scores.keys():
        if dico_scores[partie][1] == nd:
            tableau_scores.append(dico_scores[partie])
    
    # On fait un tri (ici un tri bulle) sur tableau_scores qui trie par le nombre de coups ET avec le temps de la partie (plus bas = meilleur).
    for i in range(len(tableau_scores)):
        for j in range(0, len(tableau_scores)-1-i):

            if tableau_scores[j][2] > tableau_scores[j + 1][2]:
                tableau_scores[j], tableau_scores[j + 1] = tableau_scores[j + 1], tableau_scores[j]

            elif tableau_scores[j][2] == tableau_scores[j + 1][2] and tableau_scores[j][3] > tableau_scores[j + 1][3]:
                tableau_scores[j], tableau_scores[j + 1] = tableau_scores[j + 1], tableau_scores[j]

    # affichage du tableau des scores trié
    print(f"\nTableau des scores pour {nd} disques :")
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

    # affichage du tableau des scores trié
    print("\nTableau des scores en fonction du temps :")
    i = 1
    for score in tableau_scores:
        nb = str(i) + "er " if i == 1 else str(i) + "ème"
        print(f"{nb} : {score[0]}, avec {score[3]} secondes.")
        i += 1

# PROGRAMME PRINCIPAL
print("Bienvenue dans les Tours de Hanoï")
dico_scores = {}
id_partie = 1

rejouer = "oui"
while rejouer in ["o", "O", "oui", "Oui"]:

    liste_coord_tours = []      # On vide la liste des coordonnées des tours pour éviter des bugs graphiques si jamais on change de nombre de disque à la prochaine partie

    nbdisques = 0
    while nbdisques < 2:
        try:
            nbdisques = int(input("Combien de disques souhaitez-vous ? : "))
            if nbdisques < 2:
                print("Veuillez entrer un nombre entier égal ou supérieur à 2 !")
        except:
            print("Veuillez entrer une valeur correcte (nombre entier égal ou supérieur à 2) !")

    start_time = time.time()

    # Initialisation du plateau et des disques dans l'interface de turtle
    plateau = init(nbdisques)
    dessinePlateau(nbdisques)
    dessineConfig(plateau, nbdisques)

    # Démarrage du jeu puis récupération des résultats une fois terminé
    resultat = boucleJeu(plateau, nbdisques)
    temps_de_jeu = time.time() - start_time

    if resultat[0]:                                                     # Cas de l'abandon
        print(f"Abandon de la partie après {resultat[2] - 1} coup(s).")

    elif resultat[3] + nbdisques < resultat[2]:                        # Cas de la défaite
        print(f"Perdu ! Vous avez fait trop de coups (le maximum autorisé ici était {resultat[3] + nbdisques} coups).")

    elif resultat[1]:                                                   # Cas de la victoire
        print(f"Victoire ! Gagné en {resultat[2]} coups (le minimum de coups possibles pour {nbdisques} disques étant {resultat[3]} coups).")
        nom = input("Entrez votre nom : ")
        sauvScore(dico_scores, id_partie, nom, nbdisques, resultat[2], round(temps_de_jeu, 1))

    rejouer = input("Voulez vous rejouer (Oui / Non) ? : ")
    effacePlateauDisques(nbdisques)
    id_partie += 1

dico_score_2 = {1:('ccc', nbdisques, 8, 30.7), 2:('bbb', nbdisques, 3, 21.9), 3:('aaa', nbdisques, 5, 11.7), 4:('ddd', nbdisques, 3, 11.4)}

afficheScores(dico_score_2, nbdisques)
afficheChronos(dico_score_2)