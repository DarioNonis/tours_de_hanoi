# Tours de Hanoï

Projet encadré porté sur le problème des [Tours de Hanoï](https://fr.wikipedia.org/wiki/Tours_de_Hano%C3%AF).

## Exigences

Pour faire fonctionner ce programme, il vous faut : 

 - Python 3.7 ou supérieur (le support n'est pas assuré pour les versions précédentes)
 - Le module [Turtle](https://docs.python.org/fr/3/library/turtle.html)

Il ne vous reste plus qu'à lancer le fichier `main.py`

## Rapport
 - Toutes les parties ont été implémentées (de A à F, voir le fichier [pdf](https://github.com/DarioNonis/tours_de_hanoi/blob/master/projet-inf101-hanoi.pdf)).
 - Il n'y a pas vraiment d'extensions par rapport au projet de base, si ce n'est un code très efficace (notamment avec l'interface Turtle), ainsi que l'ajout de couleurs et de différents formattages au texte affiché dans la console python pour simplifier l'UI / UX.
 - Le code ne contient pas de bugs (affirmation après de **nombreux** tests), de la gestion d'erreur a également été mise en place pour éviter toute erreur par l'utilisateur

## Explications des fonctions non évidentes
Bien que ce projet soit beaucoup commenté, certaines fonctions ou certains passages sont un peu durs à comprendre, revenons dessus :
 - La fonction `dessineDisque` est utilisée pour dessiner un disque spécifié par son numéro `nd` sur le plateau. Elle utilise 2 boucles pour parcourir le plateau et trouver le disque à dessiner. Les coordonnées (x, y) et les dimensions (longueur, largeur) du rectangle représentant le disque sont calculées en fonction de sa position sur la tour. Ces calculs intègrent des paramètres prédéfinis tels que l'épaisseur du plateau, le diamètre du plus petit disque, et l'écart entre les tours.

- Pour la fonction `dessineConfig`, à chaque itération de la boucle, la fonction `dessineDisque` est appelée, où `i` représente le numéro du disque à dessiner. Ainsi, tous les disques de la configuration sont dessinés successivement en utilisant la fonction précédemment expliquée dessineDisque.

- La fonction `solutionDeplacements` génère la liste des déplacements nécessaires pour résoudre le problème des Tours de Hanoï avec `nbdisques` disques. Elle utilise une approche récursive (ce qui veut dire qu'elle s'appelle elle-même de manière répétée avec des paramètres différents). Elle se déplace d'abord `nbdisques - 1` disques de la tour de départ à la tour du milieu, puis ajoute le déplacement du disque restant de la tour de départ à la tour d'arrivée, et enfin, déplace à nouveau les `nbdisques - 1` disques de la tour du milieu à la tour d'arrivée. Les déplacements sont stockés dans une liste `liste_deplacements` qui est passée en paramètre. Si aucune liste n'est fournie, elle est initialisée à une liste vide.

- La fonction `resolutionAutomatique` prend en charge l'exécution automatique des déplacements générés par la fonction `solutionDeplacements`. Pour ce faire, elle parcourt la liste `liste_deplacements` et effectue les actions suivantes pour chaque déplacement :

    - Elle récupère le disque à déplacer de la tour_depart ;
    - Efface le disque du plateau en utilisant la fonction `effaceDisque` ;
    - Retire le disque de la tour de départ et l'ajoute à la tour d'arrivée dans le plateau ;
    - Et enfin, dessine le nouvel emplacement du disque sur le plateau avec la fonction `dessineDisque`.
    - *(Un délai de 0.333 secondes entre chaque déplacement a été ajouté)*