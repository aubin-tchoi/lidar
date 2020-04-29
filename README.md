# lidar
Projet Lidar ENPC

Dans l'exécution du main il suffit de changer l'adresse "path" pour y mettre le dossier dans lequel se trouve l'ensemble des scripts.
On suppose que dans ce même dossier se trouve le dossier "Work" en ligne sur Educnet et contenant les données.

# Convention adoptées

Chaque fichier commence par un intitulé apportant des précisions sur son contenu.

Tous les angles sont exprimés en degrés (°).
Dans le système de repère choisi, theta correspond à l'azimuth et phi à l'élévation (ce n'est pas le repère sphérique classique, les formules en tiennent compte).

Les fonctions utilisées uniquement au sein d'un même fichier ne prennent pas de majuscule à leur nom, celle qui sont utilisées dans le main en prennent une.

# Ce que le main fait exactement

Il extrait les données des différents fichiers pour les enregistrer dans les array U, V, W et L.
Il représente la disposition du parc éolien si demandé, de même pour la représentation du champ des points visités par le Lidar (et enregistre la figure sous forme d'image dans un dossier ./Images le cas échéant).

Dans R se trouve les valeurs des vitesses radiales enregistrées par l'anémomètre en m/s.
R_avg et R_sigma correspondent à la moyenne et l'écart type des valeurs enregistrées.
V correspond à la vitesse enregistrée par le Lidar à l'emplacement du mât.
