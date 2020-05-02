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

path  = "/Users/Tchoi/OneDrive/1A/Lidar/"   # A modifier
path0 = path  + "Work/"
path1 = path0 + "1510301.I55"
path2 = path0 + "WLS200s-15_radial_wind_data_2015-04-13_01-00-00.csv"

# On reprend les fonctions des fichiers annexes pour lire les données

os.chdir(path)  # On modifie le répertoire courant pour le répertoire contenant les fichiers .py
from Layout import Layout
from Parseur import ParseurSonique, ParseurLidar
from Comparaison import Projection, Interpolation8
from Maillage import Maillage
from Interpret import *
# from Comparaison import Regular_steps, Interpolation_regular_steps
# from Windrose import *

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
R_avg = sum(R)/len(R)   # Moyenne sur les valeurs obtenues
R_sigma = np.sqrt(sum([(v - R_avg)**2 for v in R])/len(R)) # Ecart type sur les valeurs obtenues

# Lidar
"""
if Regular_steps(L):
    V = Interpolation_regular_steps(L,xM,yM,zM,xL,yL,zL)  # Valeur de la vitesse radiale à proximité du mât telle qu'acquise par le Lidar
"""
S, C = Interpolation8(L,xM,yM,zM,xL,yL,zL) # S : Vitesse (m/s) et C : ensemble des indices des 8 points les plus proches du mât parmi ceux pour lesquels on dispose d'une mesure Lidar

# Affichage des valeurs

print("Moyenne temporelle de la vitesse mesurée par l'anémomètre : " + str(R_avg) + " m/s")
print("Ecart type sur les mesures correspondantes : " + str(R_sigma) + " m/s")
print("Vitesse mesurée au niveau du mât par le Lidar moyennée à partir de valeurs prises à proximité du mât : " + str(S) + " m/s")
plt.plot(np.arange(0,len(R)),R)
plt.xlabel("t (u.a.)")
plt.ylabel("RWS (m/s)")
plt.title("Evolution de la vitesse radiale mesurée par l'anémomètre")
plt.show()
Histo(R, R_avg, 50)
