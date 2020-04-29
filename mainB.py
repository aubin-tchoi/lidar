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

path0  = path  + "Lidar+Sonic/"

S = []
R = []
R_avg = []
R_sigma = []

for indice in range(1,9):

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
