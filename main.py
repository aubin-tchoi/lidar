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

path  = "/Users/Tchoi/OneDrive/1A/Lidar/"   # A modifier
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
R_avg = np.average(R)

# Lidar

C = Interpolationh(L,xM,yM,zM,xL,yL,zL,True) # Ensemble des indices des points vérifiant une certaine condition sur rho, theta et phi
D = [[Distance(xM-xL,yM-yL,zM-zL,L[1][C[i][j]],L[2][C[i][j]],L[3][C[i][j]]) for j in range(len(C[i]))] for i in range(len(C))]

# Valeurs à comparer

VL  = np.array([np.average([-L[4][C[i][j]] for j in range(len(C[i]))], weights = D[i]) for i in range(len(C))])
DVL = np.array([Average(L,C[k],xM,yM,zM)[1] for k in range(len(C))])
Cluster = np.array([np.array([R[int(L[0][k])] for k in range(np.amin(C[i]) - 50, np.amax(C[i]) + 50)]) for i in range(len(C))])
VS  = np.array([np.average(Cluster[i]) for i in range(len(C))])
DVS = np.array([np.sqrt(np.sum([(Cluster[i][j] - VS[i])**2 for j in range(len(Cluster[i]))])/len(Cluster[i])) for i in range(len(VS))])

# ---------- Affichage des valeurs ----------

fig, axes = plt.subplots(1, 1, num = "RWS_Sonic",figsize = (14,14))
axes.plot(np.arange(0,len(R))/10,R)
axes.set_xlabel("t (s)")
axes.set_ylabel("RWS (m/s)")

# On ajoute en rouge les points correspondant aux valeurs mesurées par le Lidar

tmptime = []
tmplidar = []
for i in range(len(C)):
    for j in range(len(C[0])):
        tmptime.append(L[0][C[i][j]]/10)
        tmplidar.append(-L[4][C[i][j]])
axes.scatter(tmptime, tmplidar, s = 14, c = 'r',zorder = 3)

axes.set_title("Evolution de la vitesse radiale mesurée par l'anémomètre")

# On enregistre temporairement les images afin de les intégrer au fichier Excel crée par la suite

if not os.path.exists(path + "Temp/"):
    os.makedirs(path + "Temp/")
fig.savefig(path + "Temp/" + "RWS_Sonic.png", dpi = 100) # Vitesse radiale

Histo(R, R_avg, VL, 70)
plt.savefig(path + "Temp/" + "Histo.png", dpi = 100) # Histogramme des valeurs

# ---------- Ecriture d'un fichier Excel ----------

# Fonction qui prend en entrée un tableau et qui modifie ses valeurs pour en garder les n premières décimales

def decimals(A, n):
    if isinstance(A, (np.ndarray, list)):
        B = []
        for k in range(len(A)):
            B.append(decimals(A[k], n))
        return np.array(B)
    elif isinstance(A, (int, float, np.intc, np.single, np.int32, np.int64, np.float32, np.float64)):
        return round(A*10**n)/10**n
    else:
        return A

workbook = xlsxwriter.Workbook('Lidar.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column(0, 7, 10) # On agrandit la largeur des colonnes

worksheet.write_row(0,0,["Time", "RWS (Lidar)", "DRWS (Lidar)","RWS (Sonic)", "DRWS (Sonic)", "Distance (m)", "rho (m)", "theta (°)", "All speeds in m/s"]) # Première ligne

row, col = 1, 0
for i in range(len(C)):
    for j in range(len(C[0])):
        worksheet.write_row(row, col, decimals([str(int((L[0][C[i][j]]/10)//60)) + " min " + str(int(10*(L[0][C[i][j]]/10)%60)/10) + " s", -L[4][C[i][j]], L[5][C[i][j]], "", "", Distance(xM-xL,yM-yL,zM-zL,L[1][C[i][j]],L[2][C[i][j]],L[3][C[i][j]]), L[1][[C[i][j]]], L[2][C[i][j]]], 4))
        row += 1
    worksheet.write_row(row, col, decimals(["Average of 4", VL[i], DVL[i], VS[i], DVS[i]], 4))
    row += 2

# Insertion des images enregistrées précédemment

worksheet.insert_image("J2", path + "Temp/" + "RWS_Sonic.png", {'x_scale': 0.33, 'y_scale': 0.33})
worksheet.insert_image("J26", path + "Temp/" + "Histo.png", {'x_scale': 0.33, 'y_scale': 0.33})

workbook.close()

# On supprime les images enregistrées

try:
    os.remove(path + "Temp/" + "Histo.png")
    os.remove(path + "Temp/" + "RWS_Sonic.png")
    os.rmdir(path + "Temp")
except FileNotFoundError:
    os.rmdir(path + "Temp")
