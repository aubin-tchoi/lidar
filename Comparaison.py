# Comparaison des valeurs de vent obtenues

import numpy as np
import time


# Calcul des coordonnées sphériques (rad) d'un point désigné par ses coordonnées cartésiennes

def cart_to_pol(x,y,z,xL,yL,zL):
    rho   = np.sqrt((x-xL)**2 + (y-yL)**2 + (z-zL)**2)
    theta = np.arctan((x-xL)/(y-yL))
    phi   = np.arcsin((z-zL)/rho)
    return rho, theta, phi


# Renvoit un vecteur contenant la composante radiale du vent mesuré par l'anémomètre

def Projection(U,V,W,xM,yM,zM,xL,yL,zL):
    rho, theta, phi = cart_to_pol(xM,yM,zM,xL,yL,zL) # Passage en coordonnées cartésiennes
    R0 = []
    for k in range(len(U)):
        R0.append(U[k]*np.sin(theta)*np.cos(phi) + V[k]*np.cos(theta)*np.cos(phi) + W[k]*np.sin(phi))
    return np.array(R0)


# Calcul de la distance euclidienne entre deux points (theta et phi à exprimer en °)

def Distance(xM,yM,zM,rho,theta,phi):
    theta = theta*np.pi/180
    phi   = phi*np.pi/180
    return np.sqrt((rho*np.sin(theta)*np.cos(phi) - xM)**2 + (rho*np.cos(theta)*np.cos(phi) - yM)**2 + (rho*np.sin(phi) - zM)**2)


# Renvoit la liste des indices des points les plus proches du mât

def Interpolation(L,xM,yM,zM,xL,yL,zL,n,count_time):
    tini = time.perf_counter()
    # La liste C va contenir les indices des points les plus proches du mât
    C = [[k,Distance(xM-xL,yM-yL,zM-zL,L[1][k],L[2][k],L[3][k])] for k in range(n)]
    C = sorted(C, key = lambda J: J[1]) # On range cette liste par distance
    for k in range(n,len(L[0])):
        for l in range(len(C)):
            d = Distance(xM-xL, yM-xL, zM-zL, L[1][k], L[2][k], L[3][k])
            if d < C[l][1]:
                C.insert(l,[k,d]) # La liste reste rangée par distance
                C.pop()
                break
    if count_time:
        print("Temps d'exécution de la fonction Interpolation : " + str(time.perf_counter() - tini) + " s")
    return same_scan([C[p][0] for p in range(len(C))])

"""
# Les deux fonctions Pas renvoient un tuple correspondant aux intervalles entre chaque mesure de r, de theta ou de phi (min(abs(a-b)) pour a,b dans liste tels que a != b)

def step_quicksort(L, count_time):  # Cette version utilise un quicksort

    tini = time.perf_counter()

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

    r0, theta0, phi0 = np.unique(L[1]), np.unique(L[2]), np.unique(L[3])   # Contiennent les différentes valeurs de r, theta et phi (sans doublon)

    r, theta, phi = quicksort(r0), quicksort(theta0), quicksort(phi0)

    # Le plus petit écart se trouvera nécessairement entre 2 valeurs consécutives après quicksort
    # dr     = min([r[k] - r[k-1] for k in range(2,len(r))])
    # dtheta = min([theta0[k] - theta0[k-1] for k in range(2,len(theta0))])
    # dphi   = min([phi[k] - phi[k-1] for k in range(2,len(phi))])

    dr, dtheta, dphi = r[1] - r[0], theta[1] - theta[0], phi[1] - phi[0]

    if count_time:
        print("Temps d'exécution de la fonction Interpolationh : " + str(time.perf_counter() - tini) + " s")

    return [dr, round(1000*dtheta)/1000, dphi]


def step(L, count_time): # Cette version n'utilise pas de quicksort

    tini = time.perf_counter()

    r0, theta0, phi0 = np.unique(L[1]), np.unique(L[2]), np.unique(L[3])   # Contiennent les différentes valeurs de r, theta et phi (sans doublon)

    dr     = (max(r0) - min(r0))/(len(r0)-1)    # len(r0)-1 puisque l'on compte le nombre d'intervalles
    dtheta = (max(theta0) - min(theta0))/(len(theta0)-1)
    dphi   = (max(phi0) - min(phi0))/(len(phi0)-1)

    if count_time:
        print("Temps d'exécution de la fonction step : " + str(time.perf_counter() - tini) + " s")

    return [dr, dtheta, dphi]


# Vérifie que r, theta et phi évoluent par pas réguliers

def Regular_steps(L):
    N = len(L[0])
    dr, dtheta, dphi = step_quicksort(L,False)
    bool = [True, True, True]
    for k in range(N):
        if abs(L[1][k]/dr - int(L[1][k]/dr)) > 0.001:   # L[5][k]/dr est entier si sa partie décimale est égale à 0
            print("r n'évolue pas par pas réguliers")
            print("Pas : " + str(dr) + ", " + "r = " + str(L[1][k]))
            bool[0] = False
            break
    else:
        print("r évolue par pas réguliers")
    for k in range(N):
        if abs(L[2][k]/dtheta - int(L[2][k]/dtheta)) > 0.001:
            print("theta n'evolue pas par pas réguliers")
            print("Pas : " + str(dtheta) + ", " + "theta = " + str(L[2][k]))
            bool[1] = False
            break
    else:
        print("theta évolue par pas réguliers")
    for k in range(N):
        if abs(L[3][k]/dphi - int(L[3][k]/dphi)) > 0.001:
            print("phi n'evolue pas par pas réguliers")
            print("Pas : " + str(dphi) + ", " + "phi = " + str(L[3][k]))
            bool[2] = False
            break
    else:
        print("phi évolue par pas régulier")
    return bool
"""

def Interpolationh(L,xM,yM,zM,xL,yL,zL,count_time):
    tini = time.perf_counter()
    rho, theta, phi = cart_to_pol(xM,yM,zM,xL,yL,zL)
    # dr, dtheta, dphi = Pas(L)
    dr, dtheta = 50, 1.2
    theta = theta*180/np.pi
    C = []  # Liste des points proches du mât
    for k in np.where(abs(L[3] - 3.96) < 0.05)[0]:
        if abs(L[1][k] - rho) <= dr/2 and abs(L[2][k] - theta) <= dtheta/2:
            C.append(k)
    if count_time:
        print("Temps d'exécution de la fonction Interpolationh : " + str(time.perf_counter() - tini) + " s")
    return same_scan(C)


# Prend en entrée une liste d'indices de mesures Lidar et renvoit une liste qui regroupe ces indices par scan

def same_scan(C0):
    rC, C, temp = 0, [], []
    C0.sort()
    for k in range(len(C0)-1):
        temp.append(C0[k])
        if (k+1)%4 == 0: # On prend les valeurs correspondant à un même scan
            C.append(np.array(temp))
            temp = []
            rC += 1
    return np.array(C)
