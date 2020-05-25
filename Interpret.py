# Fonctions utiles à l'interprétation des données

import numpy as np
import matplotlib.pyplot as plt
from numpy import cos, sin, pi
import matplotlib.cm as cm
from windrose import WindroseAxes
import os
try:
    from inspect import cleandoc as dedent
except ImportError:
    from matplotlib.cbook import dedent

# Calcul du nombre de rayons différents parcourus pour une même valeur de theta et phi

def Depth(L):
    D = []
    n = 20 # Nombre de tirages aléatoires du point de départ
    for k in range(n):
        c = np.random.randint(0,len(L[0]))  # Le point de départ est choisi aléatoirement
        while L[1][c-1] < L[1][c]:          # On se place au début d'une série de mesures à theta et phi fixés
            c -= 1
        d = 0
        while L[1][c+1] > L[1][c]:          # On compte le nombre de valeurs que prend rho pour cette série
            c += 1
            d += 1
        D.append(d)
    return int(sum(D)/len(D))                    # On regarde la moyenne des valeurs obtenues


# Nombre d'occurences d'un pas de temps entre 2 mesures et pas de temps associé (en dixièmes de s)

def MeasuringTime(L):
    TL = [L[0][k+1] - L[0][k] for k in range(int(len(L[0])-1))]
    return [[len(TL) - np.count_nonzero(TL - np.linspace(val,val,len(TL))),val] for val in np.unique(TL)]


# Visualisation d'un histogramme des valeurs de vitesses radiales mesurées par l'anémomètre

def Histo(R, n, R_avg = False, VL = False): # n : nombre de barres

    plt.figure("Histogramme", figsize = (14,14))
    H = np.zeros(n)
    rmin, rmax = min(R), max(R)

    # Remplissage de l'histogramme (j'ai comparé le temps d'exécution des deux méthodes ci dessous à l'aide de time.perf_counter() pour n = 20, 50, 100, la méthode que j'ai gardée est en moyenne 2.5 fois plus rapide et l'écart se creuse pour n grand (testé sur 50 essais à chaque fois)
    """
    for i in range(n):
        H[i] = np.size(np.where([R[k] for k in np.where(R >= rmin + i*(rmax-rmin)/n)[0]] < rmin + (i+1)*(rmax-rmin)/n)[0])
    """
    for r in R:
        if r == rmax:
            H[-1] += 1 # Il n'y a que n barres et la valeur rmax est la seule qui tomberait sur la (n+1)ème barre
        else:
            H[int(n*(r-rmin)/(rmax-rmin))] += 1
    H = H/len(R)    # On observe la proportion de valeur de R qui tombent dans chaque intervalle i*(rmax-rmin)/n

    plt.bar(np.linspace(rmin,rmax,n), H, width = 4/n)

    # Ajout d'une barre rouge pour la moyenne

    if not isinstance(R_avg, bool):
        M = np.zeros(2*n)
        M[int(2*n*(R_avg - rmin)/(rmax - rmin))] = max(H)
        plt.bar(np.linspace(rmin,rmax,2*n), M, color = 'r', width = 2/n)

    # Ajout de barres vertes pour le Lidar

    if not isinstance(VL, bool):
        try:
            li = np.zeros(2*n)
            for v in VL:
                if v < rmax:
                    li[int(2*n*(v - rmin)/(rmax - rmin))] += 2*max(H)/len(VL)
            plt.bar(np.linspace(rmin,rmax,2*n), li, color = 'g', width = 2/n)
        except IndexError:
            print("Some of the RWS values measured by the Lidar are out of the interval [min(R),max(R)]")

    plt.xlabel("Répartition des valeurs de vitesse radiale mesurées par l'anémomètre Sonic")
    k = 1 # Nombre de décimales affichées en abscisses
    plt.xticks(np.linspace(rmin,rmax,int(n/2)), [str(round(10**k*el)/10**k) for el in np.linspace(rmin,rmax,int(n/2))])


# Représentation des points en lesquels on dispose d'une mesure Lidar

# n : Nombre de points tracés
# s : rayon des points
# pause : durée de la pause entre chaque tracé de point
# xL, yL, zL : coordonnées du Lidar
# xM, yM, zM : coordonnées du mât

def Maillage(L,n,s,pause,xL,yL,zL,xM,yM,zM,show = False):
    _, (ax1, ax2) = plt.subplots(1, 2, sharex = True, num = "Maillage", figsize = (14,14)) # Les deux graphes partageront la même abscisse x
    ax1.set_title("y, x") # Le graphe de gauche représentera y en ordonnées
    ax2.set_title("z, x") # Le graphe de droite représentera z en ordonnées
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax2.set_xlabel("x")
    ax2.set_ylabel("z")
    # On représente le mât en vert et en beaucoup plus gros
    ax1.scatter(xM, yM, s = 5*s, color = 'g', alpha = 0.75)
    ax2.scatter(xM, zM, s = 5*s, color = 'g', alpha = 0.75)
    for i in range(n):
        i = 17*i # On ne prend qu'une valeur sur 17 afin de conserver une certaine lisibilité
        rho = L[1][i]
        theta = pi*L[2][i]/180
        phi = pi*L[3][i]/180
        x = rho*sin(theta)*cos(phi) + xL # Coordonnées cartésiennes
        y = rho*cos(theta)*cos(phi) + yL
        z = rho*sin(phi) + zL
        ax1.scatter(x, y, s = s, color = 'b', alpha = 0.75)
        ax2.scatter(x, z, s = s, color = 'b', alpha = 0.75)
        if show:
            plt.pause(pause)

def MaillageReduit(L,s,xL,yL,zL,xM,yM,zM,C,save = False, show = False):
    _, (ax1,ax2) = plt.subplots(1, 2, num = "MaillageReduit", figsize = (14,14))
    ax1.set_title("y, x") # Le graphe représentera x en abscisses et y en ordonnées
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax2.set_title("y, x") # Le graphe représentera x en abscisses et y en ordonnées
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    # On représente le mât en vert et en beaucoup plus gros, ainsi que le lidar, en rouge
    ax1.scatter(xM, yM, s = 2*s, color = 'g', alpha = 0.75)
    ax1.scatter(xL, yL, s = 5*s, color = 'r', alpha = 0.75)
    ax2.scatter(xM, yM, s = 15*s, color = 'g', alpha = 0.75)
    for j in range(len(C[0])):
        rho = L[1][C[0][j]]
        theta = pi*L[2][C[0][j]]/180
        phi = pi*L[3][C[0][j]]/180
        x = rho*sin(theta)*cos(phi) + xL # Coordonnées cartésiennes
        y = rho*cos(theta)*cos(phi) + yL
        z = rho*sin(phi) + zL
        ax1.scatter(x, y, s = s, color = 'b', alpha = 0.75)
        ax2.scatter(x, y, s = 3*s, color = 'b', alpha = 0.75)
    if not isinstance(save,bool):
        if not os.path.exists(save + "Images/"):
            os.makedirs(save + "Images/")
        _.savefig(save + "Images/" + "MaillageReduit.png", dpi = 100)
    if show:
        plt.show()


# Rose des vents

def norme(x,y):
    return np.sqrt(x**2+y**2)

def theta(x,y):
    return np.pi + np.arccos(x/norme(x,y)) # (U,V) dans le plan inférieur

def Windrose1(U, V, save = False, show = False):

    theta0 = theta(U,V)
    D = norme(U,V)
    if min(theta0) < 0:
        theta0 += 2*np.pi # On prend des valeurs dans [0;2pi]

    cm = plt.cm.get_cmap('Spectral')
    fig = plt.figure("Windrose1")
    ax = plt.subplot(111, projection = 'polar')
    sc = ax.scatter(theta0, D, s = 10, c=D, cmap=cm) # La couleur dépend de la norme, tout comme la distance au centre
    plt.colorbar(sc)

    # Enregistrement de l'image dans un dossier Images
    if not isinstance(save, bool):
        if not os.path.exists(save + "Images/"):
            os.makedirs(save + "Images/")
        fig.savefig(save + "Images/" + "Windrose1.png", dpi = 100)

    # Affichage de l'image
    if show:
        plt.show()


def Windrose2(U, V, nzones, save = False, show = False):   # Windrose contenant uniquement la direction du vent (pas sa norme)

    count = np.zeros(nzones)

    theta_deg = theta(U,V)*180/np.pi # Contient les valeurs des angles des vecteurs (U,V) dans le plan hz en °
    if min(theta_deg) < 0:
        theta_deg += 360

    # Décompte (histogramme par angle)
    for angle in theta_deg:
        k = int(angle//(360/nzones)) # Indice de la zone dans laquelle se trouve angle
        count[k] += 1
    densite = count/len(U)

    t = np.array([360/nzones*k for k in range(0,nzones)])*np.pi/180.0 # 360/nzones : largeur d'une zone
    fig = plt.figure("Windrose2")
    ax = plt.subplot(111, projection='polar')
    ax.set_thetagrids(angles=np.arange(0, 360, 45), labels=["E", "N-E", "N", "N-W", "W", "S-W", "S", "S-E"])
    ax.bar(t, densite*100, width = 2*np.pi/nzones, linewidth = 0.05, fc = "m") # Chaque zone occupe 1/nzones du cercle

    # Enregistrement de l'images dans un dossier Images
    if not isinstance(save, bool):
        if not os.path.exists(save + "Images/"):
            os.makedirs(save + "Images/")
        fig.savefig(save + "Images/" + "Windrose2.png", dpi = 100)

    # Affichage de l'image
    if show:
        plt.show()
