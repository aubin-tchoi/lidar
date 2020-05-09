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

# On reprend les fonctions des fichiers annexes pour lire les données
tini = time.perf_counter()
os.chdir(path)  # On modifie le répertoire courant pour le répertoire contenant les fichiers .py
from Layout import Layout
from Parseur import ParseurSonique, ParseurLidar
from Comparaison import Projection, Interpolation, Interpolationh, Average
from Maillage import Maillage

path0 = path + "Lidar+Sonic/"

os.chdir(path0)
n = len(os.listdir())//2 # On compte le nombre de fichiers (de couples de fichiers Lidar/Sonique)

workbook = xlsxwriter.Workbook(path + 'Lidar8.xlsx')
worksheet = workbook.add_worksheet()
for c in range(6*n):
    if c%6 == 0:
        worksheet.set_column(c, c, 13.66)
    else:
        worksheet.set_column(c, c, 10.5)
row, col = 0, 0

zM = 55 # Altitude du mât
zL = 0  # Altitude du Lidar

xM,yM,xL,yL = Layout(path + "Work/",False) # Coordonnées du mât et du Lidar
plt.close("Layout")

for indice in range(1, n+1): # On parcourt les différents fichiers

    path1  = path0 + "151030" + str(indice) + ".I55"
    path2  = path0 + "WLS200s-15_radial_wind_data_2015-04-13_0" + str(indice) + "-00-00.csv"

    # Champs des vitesses

    try:
        U,V,W = ParseurSonique(path1)
        L     = ParseurLidar(path2)
        L[0] %= 36000
    except FileNotFoundError:
        print("Error in path spelling")
        sys.exit()

    """
    # Il faudra adapter le rapport 850 introduit dans la ligne suivante en fonction des performances de la machine et de les indices des 8 points les plus proches du mât
    Maillage(L,int(len(L[0])/340),4,0.0001,xL,yL,zL,xM,yM,zM) # On ne représente qu'un point sur 17 afin de conserver une certaine lisibilité

    if not os.path.exists(path + "Images/"):
        os.makedirs(path + "Images/")
    plt.savefig(path + "Images/" + "Champ_Lidar_" + str(indice) + ".png")

    plt.close("Maillage") # La figure se ferme juste après avoir fini de tracer afin d'éviter de surcharger l'instance de python ouverte (elle garde en mémoire tous les points pendant toute la durée du tracé)
    """
    # ---------- Traitement des données ----------

    # Anémomètre sonique

    R = Projection(U,V,W,xM,yM,zM,xL,yL,zL)*(1/100) # Valeurs des vitesses radiales acquises par l'anémomètre (en m/s)
    R_avg = sum(R)/len(R)

    # Lidar

    # C = Interpolation(L,xM,yM,zM,xL,yL,zL,16,True) # Ensemble des indices des 16 points les plus proches du mât
    C = Interpolationh(L,xM,yM,zM,xL,yL,zL,False) # Ensemble des indices des points vérifiant une certaine condition sur rho, theta et phi

    # Valeurs à comparer

    VL  = np.array([Average(L,C[k],xM,yM,zM)[0] for k in range(len(C))])
    DVL = np.array([Average(L,C[k],xM,yM,zM)[1] for k in range(len(C))])
    VS  = np.array([sum([(R[int(L[0][C[i][j]-1])] + R[int(L[0][C[i][j]])] + R[int(L[0][C[i][j]+1])])/3 for j in range(len(C[i]))])/len(C[i]) for i in range(len(C))]) # On moyenne sur 3 valeurs proches dans le temps puisque les horloges des deux appareils de mesure peuvent être désynchronisées

    worksheet.write_row(row,col,[str(indice-1) + ":00 to " + str(indice) + ":00 a.m.", "Time", "RWS (Lidar)", "DRWS (Lidar)", "RWS (Sonic)"])
    row += 1
    col += 1
    for i in range(len(C)):
        for j in range(len(C[0])):
            worksheet.write_row(row, col, [str(int((L[0][C[i][j]]/10)//60)) + " min " + str(int(10*(L[0][C[i][j]]/10)%60)/10) + " s", -L[4][C[i][j]], L[5][C[i][j]], (R[int(L[0][C[i][j]-1])] + R[int(L[0][C[i][j]])] + R[int(L[0][C[i][j]+1])])/3])
            row += 1
        worksheet.write_row(row, col, ["Average of 4", VL[i], DVL[i], VS[i]])
        row += 2
    col += 5
    row = 0

    if indice == 1:
        print(str(indice) + "er fichier traité !")
    else:
        print(str(indice) + "ème fichier traité !")

workbook.close()
print("Total execution time : " + str(time.perf_counter() - tini) + " s")
