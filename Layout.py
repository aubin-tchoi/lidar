## Représentation de la disposition du parc éolien

import os
import re
import matplotlib.pyplot as plt
import docx2txt

# path = "/Users/aubin/OneDrive/1A/Lidar/Work/"

def Layout(path):
    
    # Conversion du .docx en .txt
    
    MY_TEXT = docx2txt.process(path + "coordx_y_mat_eoliennes_ls.docx")

    with open(path + "coordx_y_mat_eoliennes_ls.txt", "w") as text_file:
        print(MY_TEXT, file=text_file)

    # Fonctions utiles

    def skipline(n):
        for i in range(n):
            file.readline()

    def placepoint(color): # Suppose que les deux prochaines lignes contiennent les coordonnées du point à placer
        line = file.readline()
        x = float(line)
        line = file.readline()
        y = float(line)
        plt.scatter(x,y,c=color)
        return x,y
    
    # Lecture du fichier

    file = open(path + "coordx_y_mat_eoliennes_ls.txt")

    with open(path, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != '\n':
                f.write(i)
        f.truncate()

    skipline(2)
    placepoint('g')        # Mât en vert

    skipline(1)
    x,y = placepoint('r')        # Lidar en rouge

    line = file.readline()
    n = 8                  # Nombre d'éoliennes

    for i in range(n):     # Présenté sous le format : n°,x,y,z,45 donc on skip 1 ligne avant de placer le point et 2 après
        skipline(1)
        placepoint('b')    # Eoliennes en bleu
        skipline(2)
    
    # Affichage
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Layout du parc éolien (Mât en vert, lidar en rouge et éoliennes en bleu)')
    plt.grid()
    plt.axis('equal')
    plt.show()

    file.close()

    # Suppression du fichier .txt créé

    os.remove(path + "coordx_y_mat_eoliennes_ls.txt")
    return x,y
