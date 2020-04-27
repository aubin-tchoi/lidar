## Comparaison des valeurs de vent obtenues

import numpy as np

path  = "/Users/aubin/OneDrive/1A/Lidar/"
path0 = path  + "Work/"
path1 = path0 + "1510301.I55.txt"
path2 = path0 + "WLS200s-15_radial_wind_data_2015-04-13_01-00-00.csv"

# On reprend les fonctions des fichiers annexes pour lire les données

os.chdir(path)
from Parseur import *
from Layout import *

U,V,W = ParseurSonique(path1)
L,T   = ParseurLidar(path2)

"""
u.er = UsinOcosP + VcosOcosP + WsinP
u(k).er(l) = U[k]T[1][l]T[2][l] + V[k]T[0][k]T[2][l] + W[k]T[3][l]
-> Reste à faire le bon choix de k et l : la discrétisation des deux champs n'est pas la même,
Pour chaque point Lidar, on peut interpoler (linéairement) le champ de vitesses Sonique entre deux points proches
(proches en rho, theta et phi : rho = moyenne quad(x,y,z), theta = arctan(y/x), phi = arcsin(z/rho)
"""

xL,yL = Layout(path0,False) # rho, theta et phi sont calculés à partir de cette origine (position du lidar)

def cart_to_pol(x,y,z): # Permet d'obtenir les coordonnées en sphériques à partir de coordonnées cartésiennes
    rho = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arctan(y/x)
    phi = np.arcsin(z/rho)
    return rho, theta, phi

