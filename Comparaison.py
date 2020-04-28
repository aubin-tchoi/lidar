# Comparaison des valeurs de vent obtenues

import numpy as np


# Calcul des coordonnées sphériques d'un point désigné par ses coordonnées cartésiennes

def cart_to_pol(x,y,z,xL,yL,zL):
    rho = np.sqrt((x-xL)**2 + (y-yL)**2 + (z-zL)**2)
    theta = np.arctan((x-xL)/(y-yL))*180/np.pi
    phi = np.arcsin((z-zL)/rho)*180/np.pi
    return rho, theta, phi


# Renvoit un vecteur contenant la composante radiale du vent mesuré par l'anémomètre

def Projection(U,V,W,x,y,z,xL,yL,zL):
    rho, theta, phi = cart_to_pol(x,y,z,xL,yL,zL)
    R = []
    N = len(U)
    for k in range(N):
        R.append(U[k]*np.sin(theta)*np.cos(phi) + V[k]*np.cos(theta)*np.cos(phi) + W[k]*np.sin(phi))
    return R

# La partie qui suit permet d'obtenir un résultat rapidement en supposant que rho, theta et phi évoluent par intervalles réguliers, ce qui n'est pas le cas dans le premier exemple étudié
"""
# Renvoit un tuple correspondant aux intervalles entre chaque mesure de r, de theta ou de phi (min(a,b) pour a,b dans liste tels que a != b)

def Pas(L):
    def quicksort(x):
        if len(x) == 1 or len(x) == 0:
            return x
        else:
            pivot = x[0]
            i = 0
            for j in range(len(x)-1):
                if x[j+1] < pivot:
                    x[j+1],x[i+1] = x[i+1], x[j+1]
                    i += 1
            x[0],x[i] = x[i],x[0]
            first_part = quicksort(x[:i])
            second_part = quicksort(x[i+1:])
            first_part.append(x[i])
            return first_part + second_part

    r0, theta0, phi0 = [], [], []   # Contiendront les différentes valeurs de r, theta et phi (sans doublon)
    for k in range(len(L[0])):
        if L[5][k] not in r0:
            r0.append(L[5][k])
        if L[3][k] not in theta0:
            theta0.append(L[3][k])
        if L[4][k] not in phi0:
            phi0.append(L[4][k])

    r, theta, phi = quicksort(r0), quicksort(theta0), quicksort(phi0)
    # Le plus petit écart se trouvera nécessairement entre 2 valeurs consécutives après quicksort
    dr     = min([r[k] - r[k-1] for k in range(2,len(r))])
    dtheta = min([theta[k] - theta[k-1] for k in range(2,len(theta))])
    dphi   = min([phi[k] - phi[k-1] for k in range(2,len(phi))])
    return dr, dtheta, dphi


# Vérifie que r, theta et phi évoluent par pas réguliers

def test_pas_regulier(L):
    N = len(L[0])
    dr, dtheta, dphi = Pas(L)
    bool = True
    for k in range(N):
        if abs(L[5][k]/dr - int(L[5][k]/dr)) > 0.001:   # L[5][k]/dr est entier si sa partie décimale est égale à 0
            print("r n'évolue pas par pas réguliers")
            print("Pas : " + str(dr) + ", " + "r = " + str(L[5][k]))
            bool = False
            break
    for k in range(N):
        if abs(L[3][k]/dtheta - int(L[3][k]/dtheta)) > 0.001:
            print("theta n'evolue pas par pas réguliers")
            print("Pas : " + str(dphi) + ", " + "theta = " + str(L[3][k]))
            bool = False
            break
    for k in range(N):
        if abs(L[4][k]/dphi - int(L[4][k]/dphi)) > 0.001:
            print("phi n'evolue pas par pas réguliers")
            print("Pas : " + str(dphi) + ", " + "phi = " + str(L[4][k]))
            bool = False
            break
    return bool


# Renvoit la valeur de vitesse radiale du Lidar au niveau du mat (en interpolant des valeurs prises à proximité du mât) en supposant test_pas_regulier == True

def Interpolation_pas_regulier(L,x,y,z,xL,yL,zL):
    rho, theta, phi = cart_to_pol(x,y,z,xL,yL,zL)
    dr, dtheta, dphi = Pas(L)
    N = len(L[0])
    C = []  # Liste des points proches du mât
    for k in range(N):
        if abs(L[5][k] - rho) <= dr/2 and abs(L[3][k] - theta) <= dtheta/2 and abs(L[4][k] - phi) <= dphi/2:
            C.append(k)
    n = len(C)
    V = 0
    try:
        for k in range(n):
            V += L[6][k]
        V = V/n     # Moyenne arithmétique de la vitesse en tous les points de C (à remplacer par une autre moyenne plus représentative comme une moyenne pondérée par les distances)
    except ZeroDivisionError:
        print("Pas non régulier")
    return V
"""

# Supposons qu'on ait trouvé les 8 points les plus proches du mât parmi les points mesurés par le Lidar,
# Il faut alors moyenner les valeurs de vitesses en chacun de ces points
# Cette moyenne doit rendre compte de la position du mât dans le polygône courbé reliant ces points.

def moyenne(L, X, x, y, z):    # X correspond ici à l'ensemble des points
    d = [np.sqrt((L[5][k]*np.sin(L[3][k])*np.cos(L[4][k])-x)**2 + (L[5][k]*np.cos(L[3][k])*np.cos(L[4][k])-y)**2 + (L[5][k]*np.sin(L[4][k])-z)**2) for k in X] # Distance euclidienne
    dtot = sum(d)
    V = 0
    for k in X:
        V += L[5][k]/len(X)    # Moyenne pondérée par d
    print(d)
    return V

# Renvoit la valeur de vitesse Lidar au niveau du mât

def Interpolation8(L,x,y,z,xL,yL,zL):
    rho, theta, phi = cart_to_pol(x,y,z,xL,yL,zL)
    C = [k for k in range(8)]   # Contient les indices des 8 points plus proches du mât
    V = 0
    for k in range(8,len(L[0])):    # Complexité en O(N) (On peut optimiser mais on ne passera pas en dessous de N)
        for i in range(len(C)):
            if abs(L[5][k] - rho) < abs(L[5][C[i]] - rho) and abs(L[3][k] - theta) < abs(L[3][C[i]] - theta) and abs(L[4][k] - phi) < abs(L[4][C[i]] - phi):
                C[i] = k
                break   # On veut que C contienne des indices tous différents
    V = moyenne(L, C, x, y, z)
    print(rho,theta,phi)
    return V
