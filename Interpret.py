# Fonctions utiles à l'interprétation des données

import numpy as np
import matplotlib.pyplot as plt


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
    return sum(D)/len(D)                    # On regarde la moyenne des valeurs obtenues


# Visualisation d'un histogramme des valeurs de vitesses radiales mesurées par l'anémomètre

def Histo(R, R_avg, VL, n): # n : nombre de barres

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
    M = np.zeros(2*n)
    M[int(2*n*(R_avg - rmin)/(rmax - rmin))] = max(H)
    plt.bar(np.linspace(rmin,rmax,2*n), M, color = 'r', width = 2/n)

    # Ajout de barres vertes pour le Lidar
    L = np.zeros(2*n)
    for v in VL:
        L[int(2*n*(v - rmin)/(rmax - rmin))] += 2*max(H)/len(VL)
    plt.bar(np.linspace(rmin,rmax,2*n), L, color = 'g', width = 2/n)

    plt.xlabel("Répartition des valeurs de vitesse radiale mesurées par l'anémomètre Sonic")
    k = 1 # Nombre de décimales affichées en abscisses
    plt.xticks(np.linspace(rmin,rmax,int(n/2)), [str(round(10**k*el)/10**k) for el in np.linspace(rmin,rmax,int(n/2))])
    plt.show()

