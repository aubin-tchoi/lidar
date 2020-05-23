# Représentation des points en lesquels on dispose d'une mesure Lidar

from numpy import cos, sin, pi
import matplotlib.pyplot as plt
import os

# n : Nombre de points tracés
# s : rayon des points
# pause : durée de la pause entre chaque tracé de point
# xL, yL, zL : coordonnées du Lidar
# xM, yM, zM : coordonnées du mât

def Maillage(L,n,s,pause,xL,yL,zL,xM,yM,zM):
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
