# main

import numpy as np
import os
import builtins

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
from Lidar-Sonique import *

# Champs des vitesses

U,V,W = ParseurSonique(path1)
L,T   = ParseurLidar(path2)

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

