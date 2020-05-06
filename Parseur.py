# Extraction de données à partir des différents fichiers

import os
import numpy as np
from shutil import copyfile


# Conversion du timestamp en dixièmes de seconde écoulés depuis minuit (pour match les indices des données Sonic)

def convertime(str):
    HouMouS = str.replace(":", " ").split() # Hour, Min, Sec
    return round((float(HouMouS[0])*3600 + float(HouMouS[1])*60 + float(HouMouS[2]))*10)


# Prend en entrée un fichier contenant des données Sonic et renvoit les array U, V, W (coordonnées du vent)

def ParseurSonique(path):

    copyfile(path, path + ".txt")
    file = open(path + ".txt",'r')

    line = file.readline()                  # On passe la première ligne

    n = len(open(path).readlines()) - 1     # Nombre de lignes dans le .txt (moins la première ligne)
    U0, V0, W0 = [], [], []
    for i in range(n):
        line = file.readline()
        uvwt = line.replace(';','').replace(',',' ').split()
        U0.append(float(uvwt[0]))
        V0.append(float(uvwt[1]))
        W0.append(float(uvwt[2]))
    U = np.array(U0)                        # Vitesses en cm/s
    V = np.array(V0)
    W = np.array(W0)

    file.close()
    os.remove(path + ".txt")

    return U, V, W


# Prend en entrée un fichier contenant des données Lidar et renvoit un array [temps, rho, theta, phi, RWS, DRWS]
# Le temps est exprimé en dixièmes de s, rho en m, les angles en ° et les vitesses en m/s.

def ParseurLidar(path):

    file = open(path,'r')
    line = file.readline()                  # On passe la première ligne
    n = len(open(path).readlines()) - 1     # Nombre de lignes dans le .csv (moins la première ligne)

    time0, rho0, theta0, phi0, rws0, drws0  = [], [], [], [], [], []

    for i in range(n):
        line = file.readline()
        polar = line.replace(';',' ').replace(',',' ').split()
        if convertime(polar[1]) < 432000: # time0 correspondra à l'indice de la ligne correspondante dans les mesures Sonic (indice*10 = nbr de s écoulées depuis minuit)
            time0.append(int(convertime(polar[1])))
            rho0.append(float(polar[7]))
            theta0.append(float(polar[5]) + 180.)
            phi0.append(round(100*float(polar[6]))/100)
            rws0.append(float(polar[8]))
            drws0.append(float(polar[9]))

    L = [np.array(time0), np.array(rho0), np.array(theta0), np.array(phi0), np.array(rws0), np.array(drws0)]

    file.close()

    return np.array(L)
