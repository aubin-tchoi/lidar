# La même chose que le main appliqué aux fichiers du dossier "Lidar+Sonic"

import sys
import os
import builtins
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter
import time

"""
On se place dans le repère sphérique (r, theta, phi) ayant pour origine l'emplacement du Lidar
et dans lequel theta correspond à l'azimuth (theta = 0 pointe vers le Nord) et phi à l'élévation (phi = 0 : plan horizontal)
"""

# ---------- Initialisation ----------

path  = "/Users/aubin/OneDrive/1A/Lidar/"   # A modifier

# Initialisation du compteur de temps

tini = time.perf_counter()

os.chdir(path)  # On modifie le répertoire courant pour le répertoire contenant les fichiers .py

# On reprend les fonctions des fichiers annexes pour lire les données
from Layout import Layout
from Parseur import ParseurSonique, ParseurLidar
from Comparaison import Projection, Interpolation, Interpolationh, Distance
from Maillage import Maillage
from Interpret import *

path0 = path + "Lidar+Sonic/"

os.chdir(path0)
n = len(os.listdir())//2 # On compte le nombre de fichiers (de couples de fichiers Lidar/Sonique)

    # Fonction qui prend en entrée un tableau et qui modifie ses valeurs pour en garder les n premières décimales

def decimals(A, p):
    if isinstance(A, (np.ndarray, list)):
        B = []
        for k in range(len(A)):
            B.append(decimals(A[k], p))
        return np.array(B)
    elif isinstance(A, (int, float, np.intc, np.single, np.int32, np.int64, np.float32, np.float64)):
        return round(A*10**p)/10**p
    else:
        return A

workbook = xlsxwriter.Workbook(path + 'Lidar8.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column(0, 1, 14)
worksheet.set_column(1, 7, 10.5) # On agrandit la largeur des colonnes
worksheet.write_row(0,0,["Time", "RWS (Lidar)", "DRWS (Lidar)","RWS (Sonic)", "DRWS (Sonic)", "Distance (m)", "rho (m)", "theta (°)", "All speeds in m/s"]) # Première ligne
row, col = 1, 0

zM = 55 # Altitude du mât
zL = 0  # Altitude du Lidar

xM,yM,xL,yL = Layout(path + "Work/",False) # Coordonnées du mât et du Lidar
plt.close("Layout")

for hour in range(1, n+1): # On parcourt les différents fichiers

    path1  = path0 + "151030" + str(hour) + ".I55"
    path2  = path0 + "WLS200s-15_radial_wind_data_2015-04-13_0" + str(hour) + "-00-00.csv"

    # Champs des vitesses

    try:
        U,V,W = ParseurSonique(path1)
        L = ParseurLidar(path2)
        L[0] %= 36000
    except FileNotFoundError:
        print("Error in path spelling")
        sys.exit()

    """
    # Il faudra adapter le rapport 850 introduit dans la ligne suivante en fonction des performances de la machine et de les indices des 8 points les plus proches du mât
    Maillage(L,int(len(L[0])/340),4,0.0001,xL,yL,zL,xM,yM,zM) # On ne représente qu'un point sur 17 afin de conserver une certaine lisibilité

    if not os.path.exists(path + "Images/"):
        os.makedirs(path + "Images/")
    plt.savefig(path + "Images/" + "Champ_Lidar_" + str(hour) + ".png")

    plt.close("Maillage") # La figure se ferme juste après avoir fini de tracer afin d'éviter de surcharger l'instance de python ouverte (elle garde en mémoire tous les points pendant toute la durée du tracé)
    """

    # ---------- Traitement des données ----------


    # Lidar

    # Ensemble des indices des points vérifiant une certaine condition sur rho, theta et phi
    C = Interpolationh(L,xM,yM,zM,xL,yL,zL,False)

    # Distances auxquelles se trouvent les points de mesure par rapport au mât
    D = [[Distance(xM-xL,yM-yL,zM-zL,L[1][C[i][j]],L[2][C[i][j]],L[3][C[i][j]]) for j in range(len(C[i]))] for i in range(len(C))]

    # Vitesse Lidar
    VL = np.array([np.average([-L[4][C[i][j]] for j in range(len(C[i]))], weights = D[i]) for i in range(len(C))])

    # Ecart type sur les mesures Lidar
    DVL = np.array([np.average([L[5][C[i][j]] for j in range(len(C[i]))], weights = D[i]) for i in range(len(C))])


    # Anémomètre sonique

    # Valeurs des vitesses radiales acquises par l'anémomètre (en m/s)
    R = Projection(U,V,W,xM,yM,zM,xL,yL,zL)*(1/100)

    # Moyenne des valeurs mesurées (utilisée dans la fonction Histo)
    R_avg = np.average(R)

    # Cluster de valeurs de la vitesse Sonique prises à des temps proches de ceux auxquels le Lidar prend une mesure proche du mât
    Cluster = np.array([np.array([R[int(L[0][k])] for k in range(np.amin(C[i]) - 50, np.amax(C[i]) + 50)]) for i in range(len(C))])

    # Vitesse Sonique (moyenne par cluster)
    VS  = np.array([np.average(Cluster[i]) for i in range(len(C))])

    # Ecart type sur chaque cluster
    DVS = np.array([np.sqrt(np.sum([(Cluster[i][j] - VS[i])**2 for j in range(len(Cluster[i]))])/len(Cluster[i])) for i in range(len(VS))])


    # ---------- Ecriture du fichier Excel ----------

    for i in range(len(C)):
        for j in range(len(C[0])):
            worksheet.write_row(row, col, decimals([str(hour - 1) + " h " + str(int((L[0][C[i][j]]/10)//60)) + " min " + str(int(10*(L[0][C[i][j]]/10)%60)/10) + " s", -L[4][C[i][j]], L[5][C[i][j]], "", "", Distance(xM-xL,yM-yL,zM-zL,L[1][C[i][j]],L[2][C[i][j]],L[3][C[i][j]]), L[1][[C[i][j]]], L[2][C[i][j]]], 4))
            row += 1
        worksheet.write_row(row, col, decimals(["Average of 4", VL[i], DVL[i], VS[i], DVS[i]], 4))
        row += 2

try:
    workbook.close()
except xlsxwriter.exceptions.FileCreateError: # Résoud un problème d'autorisation rencontré sous Windows
        os.remove(path + "Lidar.xlsx") # On supprime le fichier bloqué et on le réécrit

print("Total execution time : " + str(time.perf_counter() - tini) + " s")
