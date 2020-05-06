# Projet Lidar ENPC


Dans l'exécution du main il suffit de changer l'adresse "path" pour y mettre le dossier dans lequel se trouve l'ensemble des scripts.
On suppose que dans ce même dossier se trouve le dossier "Work".

## Convention adoptées

Chaque fichier commence par un intitulé apportant des précisions sur son contenu.

Dans le système de repère choisi, theta correspond à l'azimuth et phi à l'élévation (ce n'est pas le repère sphérique classique, les formules en tiennent compte).

Les fonctions utilisées uniquement au sein d'un même fichier ne prennent pas de majuscule à leur nom, celle qui sont utilisées dans le main en prennent une.

### Ce que le main fait exactement

- Je l'ai fait crash si on lui donne le mauvais chemin,
- Il représente la disposition du parc éolien si demandé, de même pour la représentation du champ des points visités par le Lidar (et enregistre la figure sous forme d'image dans un dossier ./Images si demandé),
- Il enregistre dans un fichier .xlsx les données traités.

# Schéma explicatif

![alt text](https://github.com/aubin-tchoi/lidar/blob/master/Explication.jpg)
