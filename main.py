# main

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
path0 = path  + "Work/"
path1 = path0 + "1510301.I55"
path2 = path0 + "WLS200s-15_radial_wind_data_2015-04-13_01-00-00.csv"

# On reprend les fonctions des fichiers annexes pour lire les données

os.chdir(path)  # On modifie le répertoire courant pour le répertoire contenant les fichiers .py
from Layout import Layout
from Parseur import ParseurSonique, ParseurLidar
from Comparaison import Projection, Interpolation
from Maillage import Maillage
from Interpret import *

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
"""
rep = builtins.input("Display Windrose (Y/N) ? ") # Rose des vents

if rep.upper() == "Y"
    plot_theta(U,V,121)
    windrose0(U,V,122)
"""
# Position du mât et du Lidar

rep = builtins.input("Do you wish to display the layout of the windfarm (Y/N) ? ")

if rep.upper() == "Y" or rep.upper() == "O": # O pour ceux qui voudraient dire oui
    xM,yM,xL,yL = Layout(path + "Work/",True)
else:
    xM,yM,xL,yL = Layout(path + "Work/",False)
    plt.close("Layout")

rep = builtins.input("Do you wish to display the grid of the points measured by the Lidar (Y/N) ? ")

if rep.upper() == "Y" or rep.upper() == "O":
    sav = builtins.input("Do you wish to save it (Y/N) ? ")
    n = builtins.input("Number of points (Recommended : 800) : ") # 800 c'est pas mal
    t = builtins.input("Timestep (Recommended : 0.001) : ") # 0.001 c'est pas mal
    try:
        Maillage(L,int(n),4,float(t),xL,yL,zL,xM,yM,zM) # On ne représente qu'un point sur 17 afin de conserver une certaine lisibilité
    except ValueError:
        print("Given set of values invalid")

    # Enregistrement de la figure dans un dossier Images
    if sav.upper() == "Y" or sav.upper() == "O":
        if not os.path.exists(path + "Images/"):
            os.makedirs(path + "Images/")
        plt.savefig(path + "Images/" "Champ_Lidar.png")

    plt.close("Maillage") # La figure se ferme juste après avoir fini de tracer afin d'éviter de surcharger l'instance de python ouverte (elle garde en mémoire tous les points pendant toute la durée du tracé)


# ---------- Traitement des données ----------

# Anémomètre sonique

R = Projection(U,V,W,xM,yM,zM,xL,yL,zL)*(-1/100) # Valeurs des vitesses radiales acquises par l'anémomètre (en m/s)
R_avg = sum(R)/len(R)

# Lidar

C = Interpolation(L,xM,yM,zM,xL,yL,zL,4,True) # Ensemble des indices des 4 points proches du mât

# Valeurs à comparer

VL = np.array([-L[4][C[k]] for k in range(len(C))])
VS = np.array([(R[int(round(L[0][C[k]]-1))] + R[int(round(L[0][C[k]]))] + R[int(round(L[0][C[k]]+1))])/3 for k in range(len(C))]) # Les deux instruments peuvent être désynchronisés donc on prend la moyenne des valeurs mesurées par le Sonic aux temps L[0][C[k]]

# ---------- Affichage des valeurs ----------

plt.plot(np.arange(0,len(R))/10,R)
plt.xlabel("t (s)")
plt.ylabel("RWS (m/s)") # Distribution de Weibull
plt.title("Evolution de la vitesse radiale mesurée par l'anémomètre")
plt.show()
Histo(R, R_avg, VL, 50)

