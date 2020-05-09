# main

import sys
import os
import builtins
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter

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
from Comparaison import Projection, Interpolation, Interpolationh, Average, Distance
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

R = Projection(U,V,W,xM,yM,zM,xL,yL,zL)*(1/100) # Valeurs des vitesses radiales acquises par l'anémomètre (en m/s)
R_avg = sum(R)/len(R)

# Lidar

# C = Interpolation(L,xM,yM,zM,xL,yL,zL,16,True) # Ensemble des indices des 16 points les plus proches du mât
C = Interpolationh(L,xM,yM,zM,xL,yL,zL,True) # Ensemble des indices des points vérifiant une certaine condition sur rho, theta et phi

# Valeurs à comparer

VL  = np.array([Average(L,C[k],xM,yM,zM)[0] for k in range(len(C))])
DVL = np.array([Average(L,C[k],xM,yM,zM)[1] for k in range(len(C))])
VS  = np.array([sum([(R[int(L[0][C[i][j]-1])] + R[int(L[0][C[i][j]])] + R[int(L[0][C[i][j]+1])])/3 for j in range(len(C[i]))])/len(C[i]) for i in range(len(C))]) # On moyenne sur 3 valeurs proches dans le temps puisque les horloges des deux appareils de mesure peuvent être désynchronisées


# ---------- Affichage des valeurs ----------

plt.figure("RWS_Sonic",figsize = (14,14))
plt.plot(np.arange(0,len(R))/10,R)
plt.xlabel("t (s)")
plt.ylabel("RWS (m/s)") # Distribution de Weibull
plt.title("Evolution de la vitesse radiale mesurée par l'anémomètre")
if not os.path.exists(path + "Temp/"):
    os.makedirs(path + "Temp/")
plt.savefig(path + "Temp/" + "RWS_Sonic.png", dpi = 100)
Histo(R, R_avg, VL, 70)
plt.savefig(path + "Temp/" + "Histo.png", dpi = 100)

workbook = xlsxwriter.Workbook('Lidar.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column(0, 4, 15.11)

worksheet.write_row(0,0,["Time", "RWS (Lidar) (m/s)", "DRWS (Lidar) (m/s)", "RWS (Sonic) (m/s)", "Distance (m)"])
row, col = 1, 0
for i in range(len(C)):
    for j in range(len(C[0])):
        worksheet.write_row(row, col, [str(int((L[0][C[i][j]]/10)//60)) + " min " + str(int(10*(L[0][C[i][j]]/10)%60)/10) + " s", -L[4][C[i][j]], L[5][C[i][j]], (R[int(L[0][C[i][j]-1])] + R[int(L[0][C[i][j]])] + R[int(L[0][C[i][j]+1])])/3, Distance(xM-xL,yM-yL,zM-zL,L[1][C[i][j]],L[2][C[i][j]],L[3][C[i][j]])])
        row += 1
    worksheet.write_row(row, col, ["Average of 4", VL[i], DVL[i], VS[i]])
    row += 2

worksheet.insert_image("G2", path + "Temp/" + "RWS_Sonic.png", {'x_scale': 0.33, 'y_scale': 0.33})
worksheet.insert_image("G26", path + "Temp/" + "Histo.png", {'x_scale': 0.33, 'y_scale': 0.33})

workbook.close()

try:
    os.remove(path + "Temp/" + "Histo.png")
    os.remove(path + "Temp/" + "RWS_Sonic.png")
    os.rmdir(path + "Temp")
except FileNotFoundError:
    os.rmdir(path + "Temp")
