from turtle import *

def init(n):
    tour_de_depart = []
    for i in range(n, 0, -1):
        tour_de_depart.append(i)
    return [tour_de_depart, [], []]

def nbDisques(plateau, numtour):
    return len(plateau[numtour])

def disqueSup(plateau, numtour):
    if len(plateau[numtour]) != 0 and 0 <= numtour <= 2:
        return plateau[numtour][-1]
    return -1

def posDisque(plateau, numdisque):
    for tour in plateau:
        for disque in tour:
            if disque == numdisque:
                return tour
            
def verifDepl(plateau, nt1, nt2):
    autorise = False
    if disqueSup(nt1) < disqueSup(nt2) or disqueSup(nt2) == -1:
        autorise = True
    return autorise

def verifVictoire(plateau, n):
    liste_valide = []
    for i in range(n, 0, -1):
        liste_valide.append(i)
    if liste_valide == plateau[2]:
        return True
    return False

plateau_ord_org = (-300, -200)
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
                goto(x + longueur, y - (largeur-1))

                # print(n, nbDisques(plateau, i))

                # On redessine la tour
                hauteur_tour = 20 + (n-nbDisques(plateau, i)+1)*20
                pos_tour_x, pos_tour_y = liste_coord_tours[i]
                rectangle(pos_tour_x, pos_tour_y, 6, hauteur_tour)
                

def dessineConfig(plateau, n):
    for i in range(n+1):
        dessineDisque(i, plateau, n)         

# Exemple avec un plateau avec 5 disques :
disques = 3
dessinePlateau(disques)

plato = [[3, 2, 1], [], []]
dessineConfig(plato, disques)

effaceDisque(1, plato, disques)
plato[0].remove(1)
effaceDisque(2, plato, disques)
plato[0].remove(2)
effaceDisque(3, plato, disques)
plato[0].remove(3)


done()