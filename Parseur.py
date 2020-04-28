# Extraction de données à partir des différents fichiers

import re
import numpy as np

# path1 : adresse du fichier 1510301.I55.txt
# path2 : adresse du fichier WLS200s-15_radial_wind_data_2015-04-13_01-00-00.csv

def ParseurSonique(path):

    file = open(path,'r')

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
    return U, V, W


def ParseurLidar(path):

    file = open(path,'r')

    line = file.readline()                  # On passe la première ligne

    n = len(open(path).readlines()) - 1     # Nombre de lignes dans le .csv (moins la première ligne)

    line  = file.readline()
    polar = line.replace(';',' ').replace(',',' ').split()
    k     = len(polar)                      # Nombre de valeurs à extraire de chaque ligne (détaillées dans la première ligne)

    intorfloat = [2,3,4,13]                 # Certaines données sont entières

    # L = [Configuration ID, Scan ID, LOS ID, Azimuth (en °), Elevation (en °), Range (en m), RWS (en m/s), DRWS (en m/s), CNR (en dB), Confidence Index (en %), Mean Error, Status]
    # RWS  : Radial Wind Speed
    # DRWS : Dispersion of Radial Wind Speed
    # CNR  : Carrier to Noise Ratio

    # Azimuth   : angle entre l'objet et une direction de référence (Nord) dans le plan horizontal (theta)
    # Elévation : (phi)

    L = []
    for j in range(2,k):                    # On doit décaler de 2 puisque le timestamp comprend un espace et qu'il prend deux places dans le split
                                            # Si besoin je peux ajouter une colonne pour le timestamp, mais il faudra me préciser le format
        if j in intorfloat:
            L.append([int(polar[j])])
        elif j not in intorfloat:
            L.append([float(polar[j])])

    for i in range(n-1):
        line = file.readline()
        polar = line.replace(';',' ').replace(',',' ').split()
        if int(polar[3]) != 238:            # Un Scan ID égal à 238 correspond à une donnée non valide
            for j in range(2,k):
                if j in intorfloat:
                    L[j-2].append(int(polar[j]))
                elif j not in intorfloat:
                    L[j-2].append(float(polar[j]))
            continue

    file.close()

    return np.array(L)
