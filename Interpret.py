# Fonctions utiles à l'interprétation des données

import numpy as np


# Calcul du nombre de rayons différents parcourus pour une même valeur de theta et phi

def Depth(L):
    D = []
    for k in range(n):
        c = np.random.randint(0,len(L[0]))
        while L[5][c-1] < L[5][c]:
            c -= 1
        d = 0
        while L[5][c+1] > L[5][c]:
            c += 1
            d += 1
        D.append(d)
    return sum(D)/len(D)
