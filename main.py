# main

import numpy as np
import os
import builtins

"""
On se place dans le repère sphérique (r, theta, phi) ayant pour origine l'emplacement du Lidar
et dans lequel theta correspond à l'azimuth (theta = 0 pointe vers le Nord) et phi à l'élévation (phi = 0 : plan horizontal)
"""

# ---------- Initialisation ----------

path  = "/Users/aubin/OneDrive/1A/Lidar/"   # A modifier
path0 = path  + "Work/"
path1 = path0 + "1510301.I55.txt"
path2 = path0 + "WLS200s-15_radial_wind_data_2015-04-13_01-00-00.csv"

# On reprend les fonctions des fichiers annexes pour lire les données

os.chdir(path)
from Layout import *
from Parseur import *
from Comparaison import *
# from Windrose import *

# Champs des vitesses

U,V,W = ParseurSonique(path1)
L     = ParseurLidar(path2)

z  = 55 # Altitude du mât
zL = 0  # Altitude du Lidar

# ---------- Représentations ----------

"""
rep = builtins.input("Display Windrose (Y/N) ? ") # Rose des vents

if rep.upper() == "Y":
    plot_theta(U,V,121)
    windrose0(U,V,122)
"""
rep = builtins.input("Display Layout (Y/N) ? ") # Position du mât, du Lidar et des éoliennes

if rep.upper() == "Y":
    x,y,xL,yL = Layout(path0,True)
elif rep.upper() == "N":
    x,y,xL,yL = Layout(path0,False)

# ---------- Traitement des données ----------

# Anémomètre sonique

R = Projection(U,V,W,x,y,z,xL,yL,zL) # Valeurs des vitesses radiales acquises par l'anémomètre
R_moy = sum(R)/len(R)
R_sigma = np.sqrt(sum([v**2 for v in R]))

# Lidar
"""
if test_pas_regulier(L):
    V = Interpolation_pas_regulier(L,x,y,z,xL,yL,zL)  # Valeur de la vitesse radiale à proximité du mât telle qu'acquise par le Lidar
"""
