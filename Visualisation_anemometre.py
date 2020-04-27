# Windrose

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from windrose import WindroseAxes

# Composantes de vitesse :
# U = de l'ouest vers l'est
# V = du sud au nord
# W = de bas en haut

def norme(x,y):
    return np.sqrt(x**2+y**2)

def theta(x,y):
    return np.pi - np.arccos(x/norme(x,y)) # ici arccos bijectif car tm dans cadre inf

# Tracé des vitesses

def trace_vitesse1(U,V):
    N = len(U)
    T = np.linspace(0,N,N)
    plt.plot(T,U,'r')
    plt.plot(T,V,'g')
    plt.plot(T,W,'b')
    plt.show()

# On visualise le vecteur de coordonnes (-U,-V) car U positif, le vent vient d'Ouest donc il vient de la gauche ce qui correspond à x négatif, de même pour V

def trace_vitesse2(U,V):
    norm_horizontales = norme(U,V)
    U_norm = -U/norm_horizontales
    V_norm = -V/norm_horizontales
    plt.plot(0,0,'r+')
    plt.plot(U_norm,V_norm,'+')
    plt.show()

# On associe un vecteur vitesse aux composantes U et V-> on affiche ces points sur une carte pour savoir d'où proviennent les vents. L'échelle de couleur donne la vitesse du vent (norme du vecteur (U,V))

def plot_theta(U,V,subplot):
    N = len(U)
    theta0 = theta(U,V)
    if min(theta0) < 0:
        theta0 += 2*np.pi
    norm_horizontales = norme(U,V)
    cm = plt.cm.get_cmap('Spectral')
    ax = plt.subplot(111, projection='polar')
    sc = ax.scatter(theta0,norm_horizontales,c=norm_horizontales,cmap=cm)
    plt.colorbar(sc)
    plt.show()

# On essaie de créer une rose des vents : on compte la densité de vents qui proviennent de chaque direction (N,N-E,E, etc) en découpant un cercle en différents quartiers.

def windrose0(U,V,nbr_zones,subplot):   # Windrose "à la main" sans la valeur des vitesses

    N = len(U)
    decompte = np.zeros(nbr_zones)
    theta_deg = theta(U,-V)*180/np.pi # Contient les valeurs des angles des vecteurs (U,V) dans le plan hz en °
    if min(theta_deg) < 0:
        theta_deg += 360

    for angle in theta_deg:
        k = int(angle//(360/nbr_zones)) # Indice de la zone dans laquelle se trouve angle
        decompte[k] += 1

    densite = decompte/N
    # print(densite*100)
    t = np.array([360/nbr_zones*k for k in range(0,nbr_zones)])*np.pi/180.0 # 360/nbr_zones : largeur d'une zone
    ax = plt.subplot(subplot, projection='polar')
    ax.set_thetagrids(angles=np.arange(0, 360, 45), labels=["E", "N-E", "N", "N-W", "W", "S-W", "S", "S-E"])
    ax.bar(t, densite*100, width = 2*np.pi/nbr_zones) # Chaque zone occupe 1/nbr_zones du cercle
    plt.show()

def windrose1(U,V):     # Windrose
    theta_deg = theta(U,-V)*180/np.pi
    if min(theta_deg) < 0:
        theta_deg += 360
    ax = WindroseAxes.from_ax()
    norm_horizontales = norme(U,V)
    ax.bar(theta_deg-90, norm_horizontales, normed=True, opening=0.8)
    # ax.set_legend()
    plt.show()
