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

def rectangle(x, y, longueur, largeur, couleur="black"):      # Départ du rectangle du coin supérieur gauche !
    up()
    goto(plateau_ord_org[0] + x, plateau_ord_org[1] + y)      # Coordonnées du point supérieur gauche
    down()
    color(couleur)
    for i in range(2):
        forward(longueur)
        right(90)
        forward(largeur)
        right(90)

def dessine_plateau(n):
    # On dessine la base
    rectangle(0, 0, 60 + 3*(40 + (n-1)*30), 20)

    # On dessine les n disques sur la première tour
    x, y = 20, 20
    longueur, largeur = 40 + (n-1)*30, 20
    for i in range(n):  
        rectangle(x, y, longueur, largeur)
        x += 15
        y += 20
        longueur -= 30
    
    # On dessine les tours
    x, y = 37 + (n-1)*15, (n+1)*20
    longueur, largeur = 6, 20
    for i in range(3):
        rectangle(x, y, longueur, largeur)
        x += 60 + n*20
        largeur = (n+1)*20

    rectangle(170, 20, 120, 20)
    rectangle(310, 20, 120, 20)

plato = [[], [5], [4, 3, 2, 1]]
# print(verifVictoire(plato, 5))

dessine_plateau(4)
done()