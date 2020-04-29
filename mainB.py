# La même chose que le main appliqué aux fichiers du dossier "Lidar+Sonic"

import sys
import os
import builtins
import matplotlib.pyplot as plt
import numpy as np

"""
On se place dans le repère sphérique (r, theta, phi) ayant pour origine l'emplacement du Lidar
et dans lequel theta correspond à l'azimuth (theta = 0 pointe vers le Nord) et phi à l'élévation (phi = 0 : plan horizontal)
"""

# ---------- Initialisation ----------

path  = "/Users/aubin/OneDrive/1A/Lidar/"   # A modifier

# On reprend les fonctions des fichiers annexes pour lire les données

os.chdir(path)  # On modifie le répertoire courant pour le répertoire contenant les fichiers .py
from Layout import Layout
from Parseur import ParseurSonique, ParseurLidar
from Comparaison import Projection, Interpolation8
from Maillage import Maillage
# from Comparaison import Regular_steps, Interpolation_regular_steps
# from Windrose import *

path0 = path + "Lidar+Sonic/"

S = []
R = []
R_avg = []
R_sigma = []

os.chdir(path0)
n = len(os.listdir())//2 # On compte le nombre de fichiers (de couples de fichiers Lidar/Sonique)

for indice in range(1, n+1): # On parcourt les différents fichiers

    path1  = path0 + "151030" + str(indice) + ".I55"
    path2  = path0 + "WLS200s-15_radial_wind_data_2015-04-13_0" + str(indice) + "-00-00.csv"

    # Champs des vitesses

    try:
        U,V,W = ParseurSonique(path1)
        L     = ParseurLidar(path2)
    except FileNotFoundError:
        print("Error in path spelling")
        sys.exit()

    zM = 55 # Altitude du mât
    zL = 0  # Altitude du Lidar

    # ---------- Représentations ----------

    plt.close('all')

    # Position du mât et du Lidar
    xM,yM,xL,yL = Layout(path + "Work/",False)
    plt.close("Layout")

    # Il faudra adapter le rapport 850 introduit dans la ligne suivante en fonction des performances de la machine et de les indices des 8 points les plus proches du mât
    Maillage(L,int(len(L[0])/850),8,0.0001,xL,yL,zL,xM,yM,zM) # On ne représente qu'un point sur 17 afin de conserver une certaine lisibilité

    if not os.path.exists(path + "Images/"):
        os.makedirs(path + "Images/")
    plt.savefig(path + "Images/" + "Champ_Lidar_" + str(indice) + ".png")

    plt.close("Maillage") # La figure se ferme juste après avoir fini de tracer afin d'éviter de surcharger l'instance de python ouverte (elle garde en mémoire tous les points pendant toute la durée du tracé)

    # ---------- Traitement des données ----------

    # Anémomètre sonique

    R0 = Projection(U,V,W,xM,yM,zM,xL,yL,zL)*(-1/100)
    R.append(R0) # Valeurs des vitesses radiales acquises par l'anémomètre (en m/s)
    R_avg.append(sum(R0)/len(R0))   # Moyenne sur les valeurs obtenues
    R_sigma.append(np.sqrt(sum([(v - R_avg[-1])**2 for v in R0])/len(R0))) # Ecart type sur les valeurs obtenues

    # Lidar

    S.append(Interpolation8(L,xM,yM,zM,xL,yL,zL))

    if indice == 1:
        print(str(indice) + "er fichier traité !")
    else:
        print(str(indice) + "ème fichier traité !")

file = open(path0 + "Results.txt","w+")
file.write("Compilation of the data extracted from the files in this directory \r\n")
file.write("Average values of the radial wind speed (RWS) measured by Sonic and standard deviation associated for each set of data (DRWS) (m/s) \n")
for ks in range(n):
    file.write(str(R_avg[ks]) + " " + str(R_sigma[ks]) + "\n")
file.write("\n")
file.write("Values of the wind speed measured by Lidar at the location of the Sonic measuring device for each set of data (m/s) \n")
for kl in range(n):
    file.write(str(S[kl]) + "\n")
file.write("\n")
file.write("Values of the radial wind speed measured by Sonic \r\n")
for ks1 in range(len(R)):
    file.write("Day" + " " + str(ks1 + 1) + "\n")
    for ks2 in range(len(R[0])):
        file.write(str(R[ks1][ks2]) + " ")
    file.write("\r\n")
file.close()
