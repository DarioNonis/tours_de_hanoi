# Tours de Hanoï

Projet encadré porté sur le problème des [Tours de Hanoï](https://fr.wikipedia.org/wiki/Tours_de_Hano%C3%AF).

## Exigences

Pour faire fonctionner ce programme, il vous faut : 

 - Python 3.7 ou supérieur (le support n'est pas assuré pour les versions précédentes)
 - Le module [Turtle](https://docs.python.org/fr/3/library/turtle.html)

Il ne vous reste plus qu'à lancer le fichier `main.py`

## Rapport
 - Toutes les parties ont été implémentées (de A à F, voir le fichier [pdf](https://github.com/DarioNonis/tours_de_hanoi/blob/master/projet-inf101-hanoi.pdf)).

 - Des améliorations, notamment graphiques ont étés ajoutées : En plus d'avoir un code efficace et une exécution rapide, un soin de l'UI / UX à été apporté (bien que l'interraction avec le jeu ne se fasse que dans la console python). En effet l'ajout de couleurs et de différents formattages au texte affiché dans la console python permettent à l'utilisateur de plus rapidement comprendre le programme (si il y a une erreur, si l'information est pertinente...). De plus les disques dans l'interface Turtle sont colorés (ordre des couleurs aléatoire à chaque partie) et possèdent un numéro (qui ne sera pas obstrué par la couleur du disque) qui permet à l'utilisateur d'identifier bien plus rapidement les disques et leurs taille sur le plateau de l'interface Turtle. 

 - Le code ne contient pas de bugs (affirmation après de **nombreux** tests), de la gestion d'erreur a également été mise en place pour éviter toute erreur par l'utilisateur

## Explications des fonctions non évidentes
Bien que ce projet soit beaucoup commenté, certaines fonctions ou certains passages sont un peu durs à comprendre, revenons dessus :
 - Une fonction très utilisée dans le projet est la fonction `rectange` qui dessine un rectangle dans l'interface turtle aux coordonnées, longueur, largeur, couleur du contour, couleur intérieure et numéro passé en paramètres. On place simplement le curseur de turtle aux coordonnées (avec des coordonnées à l'origine définies par la variable `plateau_ord_org`) puis on trace le rectange et si besoin on écrit aux bonnes coordonnées (dans le milieu du rectangle) un numéro qui correspond au numéro du disque (même si la fonction ne sert pas qu'à tracer les disques).

 - La fonction `dessinePlateau` sert à dessiner la base du plateau ainsi que les tours. La longueur du plateau est calculée avec la formule `80 + 3*(40 + (n-1)*30)`, `n` étant le nombre de disques sur le plateau, la longueur 80 en début de formule sert à espacer correctement les disques, auquelle on ajoute 3 fois la longueur du plus gros disque sur le plateau, calculé avec `40 + (n-1)*30`). Les tours ont une hauteur de N+1 disques, ce qui leur permet de dépasser d'une hauteur de disque supplémentaire (20 pixels) lorsque tous les disques sont empilés sur une d'entre elle. Aussi leur position a été calculée de sorte à ce qu'elles soient centrées, ceci explique le "37" dans la formule du calcule des coordonnées des tours.

 - La fonction `dessineDisque` est utilisée pour dessiner un disque spécifié par son numéro `nd` sur le plateau. Elle utilise 2 boucles pour parcourir le plateau et trouver la place de ce disque dans la configuration du plateau. Les coordonnées (x, y) et les dimensions (longueur, largeur) du rectangle représentant le disque sont calculées en fonction de sa position sur la tour. Ces calculs intègrent des paramètres prédéfinis tels que l'épaisseur du plateau, le diamètre du plus petit disque, et l'écart entre les tours.

 - `effaceDisque` est une fonction très similaire à `dessineDisque` : elle calcule les coordonnées du disque de la même manière puis l'efface et ensuite dessine la tour qui avait étée écrasée par le disque lors de son traçage dans l'interface tutrle.

- La fonction `solutionDeplacements` résout le problème des Tours de Hanoï de manière récursive. Elle prend en compte le nombre de disques ainsi que les indices de trois tours (départ, intermédiaire, arrivée). À chaque étape, elle déplace n-1 disques de la tour de départ à la tour intermédiaire, et déplace le disque de la tour de départ à la tour d'arrivée. Puis elle déplace les n-1 disques de la tour intermédiaire à la tour d'arrivée. Ces déplacements sont stockés dans une liste, qui est renvoyée à la fin.