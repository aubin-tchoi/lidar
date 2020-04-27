## Comparaison des valeurs de vent obtenues

import numpy as np
import os
import builtins

"""
On va projeter la vitesse mesurée par l'anémomètre sur le vecteur radial :
u.er = UsinOcosP + VcosOcosP + WsinP
u(k).er(l) = U[k]T[1][l]T[2][l] + V[k]T[0][k]T[2][l] + W[k]T[3][l]
-> Reste à faire le bon choix de k et l : la discrétisation des deux champs n'est pas la même
On va choisir des lignes de L proches en rho (range), theta (azimuth) et phi (élevation)
"""

# ---------- Fonctions utiles ----------

# Calcul des coordonnées sphériques d'un point désigné par ses coordonnées cartésiennes

def cart_to_pol(x,y,z,xL,yL,zL):
    rho = np.sqrt((x-xL)**2 + (y-yL)**2 + (z-zL)**2)
    theta = np.arctan((y-yL)/(x-xL))
    phi = np.arcsin((z-zL)/rho)
    return rho, theta, phi

# ---------- Initialisation ----------

path  = "/Users/Tchoi/OneDrive/1A/Lidar/"   # A modifier
path0 = path  + "Work/"
path1 = path0 + "1510301.I55.txt"
path2 = path0 + "WLS200s-15_radial_wind_data_2015-04-13_01-00-00.csv"

# On reprend les fonctions des fichiers annexes pour lire les données

os.chdir(path)
from Parseur import *
from Layout import *
from Windrose import *

# Champs des vitesses

U,V,W = ParseurSonique(path1)
L,T   = ParseurLidar(path2)

 # rho, theta et phi sont calculés à partir de cette origine (position du lidar)

# ---------- Représentations ----------

rep = builtins.input("Windrose (Y/N) ? ")   # Rose des vents

if rep.upper() == "Y":
    plot_theta(U,V,121)
    windrose0(U,V,122)

rep = builtins.input("Layout (Y/N) ? ") # Position du mât, du Lidar et des éoliennes

if rep.upper() == "Y":
    x,y,xL,yL = Layout(path0,True)
elif rep.upper() == "N":
    x,y,xL,yL = Layout(path0,False)

rho, theta, phi = cart_to_pol(x,y,z,xL,yL,zL)
