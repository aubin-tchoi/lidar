## Lidar

import re
import numpy as np

# chemin1  = "/Users/aubin/Documents/1A/Lidar/Work/1510301.I55.txt"
# chemin2  = "/Users/aubin/Documents/1A/Lidar/Work/WLS200s-15_radial_wind_data_2015-04-13_01-00-00.csv"

def ParseurSonique(chemin):

    fichier = open(chemin,'r')

    ligne = fichier.readline()                # On passe la première ligne

    n = len(open(chemin).readlines()) - 1     # Nombre de lignes dans le .txt (moins la première ligne)
    U0, V0, W0 = [], [], []
    for i in range(n):
        ligne = fichier.readline()
        uvwt = ligne.replace(';','').replace(',',' ').split()
        U0.append(float(uvwt[0]))
        V0.append(float(uvwt[1]))
        W0.append(float(uvwt[2]))
    U = np.array(U0)                          # Vitesses en cm/s
    V = np.array(V0)
    W = np.array(W0)
    
    fichier.close()
    return U, V, W

def ParseurLidar(chemin):

    fichier = open(chemin,'r')

    ligne = fichier.readline()                # On passe la première ligne

    n = len(open(chemin).readlines()) - 1     # Nombre de lignes dans le .csv (moins la première ligne)

    ligne = fichier.readline()
    polar = ligne.replace(';',' ').replace(',',' ').split()
    k     = len(polar)                        # Nombre de valeurs à extraire de chaque ligne (détaillées dans la première ligne)

    intorfloat = [2,3,4,13]                   # Certaines données sont entières

    # L = [Configuration ID, Scan ID, LOS ID, Azimuth (en °), Elevation (en °), Range (en m), RWS (en m/s), DRWS (en m/s), CNR (en dB), Confidence Index (en %), Mean Error, Status]
    # RWS  : Radial Wind Speed
    # DRWS : Dispersion of Radial Wind Speed
    # CNR  : Carrier to     Noise Ratio

    # Azimuth   : angle entre l'objet et une direction de référence (Nord) dans le plan horizontal (theta)
    # Elévation : (phi)

    L = []
    for j in range(2,k):                      # On doit décaler de 2 puisque le timestamp comprend un espace et qu'il prend deux places dans le split
                                              # Si besoin je peux ajouter une colonne pour le timestamp, mais il faudra me préciser le format
        if j in intorfloat:
            L.append([int(polar[j])])
        elif j not in intorfloat:
            L.append([float(polar[j])])

    for i in range(n-1):
        ligne = fichier.readline()
        polar = ligne.replace(';',' ').replace(',',' ').split()
        for j in range(2,k):
            if j in intorfloat:
                L[j-2].append(int(polar[j]))
            elif j not in intorfloat:
                L[j-2].append(float(polar[j]))

    fichier.close()
    
    costheta = np.vectorize(np.cos)(L[3])
    sintheta = np.vectorize(np.sin)(L[3])
    cosphi   = np.vectorize(np.cos)(L[4])
    sinphi   = np.vectorize(np.sin)(L[4])

    return L, costheta, sintheta, cosphi, sinphi
