# main

import sys
import os
import builtins
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter
import scipy.stats as sp

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
from Comparaison import Projection, Interpolation, Interpolationh, Distance
from Maillage import *
from Interpret import *

# Champs des vitesses

try:
    U,V,W = ParseurSonique(path1)
    L     = ParseurLidar(path2)
except FileNotFoundError:
    print("Error in path spelling")
    sys.exit()

zM = 75 # Altitude du mât
zL = 0  # Altitude du Lidar


# ---------- Représentations ----------

plt.close('all')
"""
rep = builtins.input("Display Windrose (Y/N) ? ") # Rose des vents

if rep.upper() == "Y"
    plot_theta(U,V,121)
    windrose0(U,V,122)
"""
# Disposition du parc éolien

rep = builtins.input("Do you wish to display the layout of the windfarm (Y/N) ? ")

if rep.upper() == "Y" or rep.upper() == "O": # O pour ceux qui voudraient dire oui
    xM,yM,xL,yL = Layout(path + "Work/",True)
else:
    xM,yM,xL,yL = Layout(path + "Work/",False)
    plt.close("Layout")

# Maillage

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


# Lidar

# Ensemble des indices des points vérifiant une certaine condition sur rho, theta et phi
C = Interpolationh(L,xM,yM,zM,xL,yL,zL,True)

# Distances auxquelles se trouvent les points de mesure par rapport au mât
D = [[Distance(xM-xL,yM-yL,zM-zL,L[1][C[i][j]],L[2][C[i][j]],L[3][C[i][j]]) for j in range(len(C[i]))] for i in range(len(C))]

# Vitesse Lidar
VL  = np.array([np.average([-L[4][C[i][j]] for j in range(len(C[i]))], weights = D[i]) for i in range(len(C))])

# Ecart type sur les mesures Lidar
DVL = np.array([np.average([L[5][C[i][j]] for j in range(len(C[i]))], weights = D[i]) for i in range(len(C))])


# Anémomètre sonique

# Valeurs des vitesses radiales acquises par l'anémomètre (en m/s)
R = Projection(U,V,W,xM,yM,zM,xL,yL,zL)*(1/100)

# Moyenne des valeurs mesurées (utilisée dans la fonction Histo)
R_avg = np.average(R)

# Cluster de valeurs de la vitesse Sonique prises à des temps proches de ceux auxquels le Lidar prend une mesure proche du mât
Cluster = np.array([np.array([R[int(L[0][k])] for k in range(np.amin(C[i]) - 100, np.amax(C[i]) + 100)]) for i in range(len(C))])

rep = builtins.input("Average by cluster (1) or linregress on each cluster (2) ? (1/2) ? ")

if rep == "1":
    # Vitesse Sonique (moyenne par cluster)
    VS  = np.array([np.average(Cluster[i]) for i in range(len(C))])

    # Ecart type sur chaque cluster
    DVS = np.array([np.sqrt(np.sum([(Cluster[i][j] - VS[i])**2 for j in range(len(Cluster[i]))])/len(Cluster[i])) for i in range(len(VS))])

elif rep == "2":
    a, b, r = np.zeros(len(Cluster)), np.zeros(len(Cluster)), np.zeros(len(Cluster))
    for k in range(len(Cluster)):
        T = np.linspace(np.amin(C[k]) - 100, np.amax(C[k]) + 100,len(Cluster[k]))
        a[k], b[k],r[k], _, _ = sp.linregress(T, Cluster[k])


# ---------- Affichage des valeurs ----------

fig, axes = plt.subplots(1, 1, num = "RWS_Sonic",figsize = (14,14))
axes.plot(np.arange(0,len(R))/10,R)
axes.set_xlabel("t (s)")
axes.set_ylabel("RWS (m/s)")
axes.set_title("Evolution de la vitesse radiale mesurée par l'anémomètre")

# On ajoute en rouge les points correspondant aux valeurs mesurées par le Lidar

tmptime = []
tmplidar = []
for i in range(len(C)):
    for j in range(len(C[0])):
        tmptime.append(L[0][C[i][j]]/10)
        tmplidar.append(-L[4][C[i][j]])
axes.scatter(tmptime, tmplidar, s = 14, c = 'r',zorder = 3)

# On enregistre temporairement les images afin de les intégrer au fichier Excel crée par la suite

if not os.path.exists(path + "Temp/"):
    os.makedirs(path + "Temp/")
fig.savefig(path + "Temp/" + "RWS_Sonic.png", dpi = 100) # Vitesse radiale

Histo(R, 70, R_avg, VL)
plt.savefig(path + "Temp/" + "Histo.png", dpi = 100) # Histogramme des valeurs

MaillageReduit(L,30,xL,yL,zL,xM,yM,zM,C,path) # Maillage réduit

# ---------- Ecriture d'un fichier Excel ----------

# Fonction qui prend en entrée un tableau et qui modifie ses valeurs pour en garder les n premières décimales

def decimals(A, p):
    if isinstance(A, (np.ndarray, list)):
        B = []
        for k in range(len(A)):
            B.append(decimals(A[k], p))
        return np.array(B)
    elif isinstance(A, (int, float, np.intc, np.single, np.int32, np.int64, np.float32, np.float64)):
        return round(A*10**p)/10**p
    else:
        return A

# Création d'un nouveau fichier Excel dans le dossier courant (path) sous le nom "Lidar.xlsx"

try:
    workbook = xlsxwriter.Workbook("Lidar.xlsx", {'strings_to_numbers': True})
    worksheet = workbook.add_worksheet()

    worksheet.set_column(0, 8, 10.5) # On agrandit la largeur des colonnes
    worksheet.set_column(8, 9, 12)

    # Première ligne
    if rep == "1":
        worksheet.write_row(0,0,["Time", "RWS (Lidar)", "DRWS (Lidar)","RWS (Sonic)", "DRWS (Sonic)", "Distance (m)", "rho (m)", "theta (°)", "Error, RMSE (%)", "All speeds in m/s"])
    elif rep == "2":
        worksheet.write_row(0,0,["Time", "RWS (Lidar)", "DRWS (Lidar)","RWS (Sonic)", "", "Distance (m)", "rho (m)", "theta (°)", "Error, RMSE (%)", "All speeds in m/s"])

    row, col = 1, 0

    for i in range(len(C)):
        for j in range(len(C[0])):
            if rep == "2":
                VSij = a[i]*L[0][C[i][j]] + b[i]
                worksheet.write_row(row, col, decimals([str(int((L[0][C[i][j]]/10)//60)) + " min " + str(int(10*(L[0][C[i][j]]/10)%60)/10) + " s", -L[4][C[i][j]], L[5][C[i][j]], VSij , "", Distance(xM-xL,yM-yL,zM-zL,L[1][C[i][j]],L[2][C[i][j]],L[3][C[i][j]]), L[1][[C[i][j]]], L[2][C[i][j]], -abs(VL[i] - VSij)/VSij*100], 4))
            elif rep == "1":
                worksheet.write_row(row, col, decimals([str(int((L[0][C[i][j]]/10)//60)) + " min " + str(int(10*(L[0][C[i][j]]/10)%60)/10) + " s", -L[4][C[i][j]], L[5][C[i][j]], "", "", Distance(xM-xL,yM-yL,zM-zL,L[1][C[i][j]],L[2][C[i][j]],L[3][C[i][j]]), L[1][[C[i][j]]], L[2][C[i][j]]], 4))
            row += 1
        if rep == "1":
            worksheet.write_row(row, col, decimals(["Average of 4", VL[i], DVL[i], VS[i], DVS[i], "", "", "", -abs(VL[i] - VS[i])/VS[i]/6*100], 4))
        row += 2

    worksheet.write(row - 1, 9, "= SQRT(SUMSQ(I:I)/COUNTA(I:I))")

    # Insertion des images enregistrées précédemment

    worksheet.insert_image("K3", path + "Temp/" + "RWS_Sonic.png", {'x_scale': 0.33, 'y_scale': 0.33})
    worksheet.insert_image("K27", path + "Temp/" + "Histo.png", {'x_scale': 0.33, 'y_scale': 0.33})

    workbook.close()

except xlsxwriter.exceptions.XlsxFileError: # Résoud un problème d'autorisation rencontré sous Windows
    os.remove(path + "Lidar.xlsx") # On supprime le fichier bloqué et on le réécrit

# On supprime les images enregistrées

try:
    os.remove(path + "Temp/" + "Histo.png")
    os.remove(path + "Temp/" + "RWS_Sonic.png")
    os.rmdir(path + "Temp")
except FileNotFoundError:
    os.rmdir(path + "Temp")

