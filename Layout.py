# Représentation de la disposition du parc éolien

import os
import docx2txt
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set(color_codes=True)

# path : adresse du dossier Work

def Layout(path,show):

    _, ax = plt.subplots(num = "Layout")
    # Conversion du .docx en .txt

    MY_TEXT = docx2txt.process(path + "coordx_y_mat_eoliennes_ls.docx")

    with open(path + "coordx_y_mat_eoliennes_ls.txt", "w") as text_file:
        print(MY_TEXT, file=text_file)

    # Fonctions utiles

    def skipline(p):
        for i0 in range(p):
            file.readline()

    def placepoint(s,color):    # Suppose que les deux prochaines lignes contiennent les coordonnées du point à placer
        line = file.readline()
        x = float(line)
        line = file.readline()
        y = float(line)
        ax.scatter(x, y, s = s, color = color, alpha = 0.75, linewidths = 0.5, edgecolors = 'k')
        return x,y

    # Lecture du fichier

    with open(path + "coordx_y_mat_eoliennes_ls.txt", "r+") as f:
        d = f.readlines()
        f.seek(0)               # Place le curseur en 0
        for I in d:
            if I != '\n':
                f.write(I)
        f.truncate()

    file = open(path + "coordx_y_mat_eoliennes_ls.txt")

    skipline(2)
    xM, yM = placepoint(80,'g')    # Mât en vert

    skipline(1)
    xL, yL = placepoint(90,'r')  # Lidar en rouge

    line = file.readline()
    n = 8                       # Nombre d'éoliennes

    for i in range(n):          # Présenté sous le format : n°,x,y,z,45 donc on skip 1 ligne avant de placer le point et 2 après
        skipline(1)
        placepoint(60,'b')      # Eoliennes en bleu
        skipline(2)

    # Affichage

    if show:
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Layout du parc éolien (Mât en vert, lidar en rouge et éoliennes en bleu)')
        ax.grid(True)
        plt.show()
    file.close()

    # Suppression du fichier .txt créé

    os.remove(path + "coordx_y_mat_eoliennes_ls.txt")

    return xM, yM, xL, yL
