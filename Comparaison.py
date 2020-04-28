# Comparaison des valeurs de vent obtenues

import numpy as np

# Calcul des coordonnées sphériques (rad) d'un point désigné par ses coordonnées cartésiennes

def cart_to_pol(x,y,z,xL,yL,zL):
    rho   = np.sqrt((x-xL)**2 + (y-yL)**2 + (z-zL)**2)
    theta = np.arctan((x-xL)/(y-yL))
    phi   = np.arcsin((z-zL)/rho)
    return rho, theta-np.pi, phi

# Calcul de la distance euclidienne entre deux points (theta et phi à exprimer en °)

def distance(xM,yM,zM,rho,theta,phi):
    theta = (theta + 180)*np.pi/180
    phi = phi*np.pi/180
    return np.sqrt((rho*np.sin(theta)*np.cos(phi) - xM)**2 + (rho*np.cos(theta)*np.cos(phi) - yM)**2 + (rho*np.sin(phi) - zM)**2)

# Renvoit un vecteur contenant la composante radiale du vent mesuré par l'anémomètre

def Projection(U,V,W,xM,yM,zM,xL,yL,zL):
    rho, theta, phi = cart_to_pol(xM,yM,zM,xL,yL,zL)
    R0 = []
    N = len(U)
    for k in range(N):
        R0.append(U[k]*np.sin(theta)*np.cos(phi) + V[k]*np.cos(theta)*np.cos(phi) + W[k]*np.sin(phi))
    return np.array(R0)

# Supposons qu'on ait trouvé les 8 points les plus proches du mât parmi les points mesurés par le Lidar,
# Il faut alors moyenner les valeurs de vitesses en chacun de ces points
# Cette moyenne doit rendre compte de la position du mât dans le polygône courbé reliant ces points.

def moyenne(L,C,xM,yM,zM):    # C contient ici à l'ensemble des indices des points à moyenner
    d = [distance(xM,yM,zM,L[5][C[k][0]],L[3][C[k][0]],L[4][C[k][0]]) for k in range(len(C))] # Distance euclidienne
    dtot = sum(d)
    V = 0
    for k in range(len(C)):
        V += L[6][C[k][0]]/len(C)    # Moyenne pondérée par d
    return V

"""
# 1ère approche : si le pas de discrétisation des mesures est régulier, il suffit de trouver le cube dans lequel se trouve le mât, ce qui est assez facile à la difficulté près que certaines mesures peuvent manquer

# Les deux fonctions Pas renvoient un tuple correspondant aux intervalles entre chaque mesure de r, de theta ou de phi (min(a,b) pour a,b dans liste tels que a != b)

def Pas_quicksort(L):  # Cette version utilise un quicksort

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
    # dr     = min([r[k] - r[k-1] for k in range(2,len(r))])
    # dtheta = min([theta0[k] - theta0[k-1] for k in range(2,len(theta0))])
    # dphi   = min([phi[k] - phi[k-1] for k in range(2,len(phi))])

    dr, dtheta, dphi = r[1] - r[0], theta[1] - theta[0], phi[1] - phi[0]
    return [dr, dtheta, dphi]

def Pas(L): # Cette version n'utilise pas de quicksort

    r0, theta0, phi0 = [], [], []   # Contiendront les différentes valeurs de r, theta et phi (sans doublon)
    for k in range(len(L[0])):
        if L[5][k] not in r0:
            r0.append(L[5][k])
        if L[3][k] not in theta0:
            theta0.append(L[3][k])
        if L[4][k] not in phi0:
            phi0.append(L[4][k])

    dr     = (max(r0) - min(r0))/(len(r0)-1)    # len(r0)-1 puisque l'on compte le nombre d'intervalles
    dtheta = (max(theta0) - min(theta0))/(len(theta0)-1)
    dphi   = (max(phi0) - min(phi0))/(len(phi0)-1)
    return [dr, dtheta, dphi]

# Vérifie que r, theta et phi évoluent par pas réguliers

def test_pas_regulier(L):
    N = len(L[0])
    dr, dtheta, dphi = Pas(L)
    bool = [True, True, True]
    for k in range(N):
        if abs(L[5][k]/dr - int(L[5][k]/dr)) > 0.001:   # L[5][k]/dr est entier si sa partie décimale est égale à 0
            print("r n'évolue pas par pas réguliers")
            print("Pas : " + str(dr) + ", " + "r = " + str(L[5][k]))
            bool[0] = False
            break
    else:
        print("r évolue par pas réguliers")
    for k in range(N):
        if abs(L[3][k]/dtheta - int(L[3][k]/dtheta)) > 0.001:
            print("theta n'evolue pas par pas réguliers")
            print("Pas : " + str(dphi) + ", " + "theta = " + str(L[3][k]))
            bool[1] = False
            break
    else:
        print("theta évolue par pas réguliers")
    for k in range(N):
        if abs(L[4][k]/dphi - int(L[4][k]/dphi)) > 0.001:
            print("phi n'evolue pas par pas réguliers")
            print("Pas : " + str(dphi) + ", " + "phi = " + str(L[4][k]))
            bool[2] = False
            break
    else:
        print("phi évolue par pas régulier")
    return bool

# Renvoit la valeur de vitesse Lidar au niveau du mât

def Interpolation_pas_regulier(L,x,y,z,xL,yL,zL):
    dr, dtheta, dphi = Pas(L)
    N = len(L[0])
    C = []  # Liste des points proches du mât
    for k in range(N):
        if abs(L[5][k] - rho) <= dr/2 and abs(L[3][k] - theta) <= dtheta/2 and abs(L[4][k] - phi) <= dphi/2:
            C.append(k)
    return moyenne(L, C, x, y, z)
"""

# 2ème approche : on détermine directement les 8 points les plus proches du mât

def Interpolation8(L,xM,yM,zM,xL,yL,zL):
    # La liste C va contenir les indices des points les plus proches du mât
    C = [[k,distance(xM-xL,yM-yL,zM-zL,L[5][k],L[3][k],L[4][k])] for k in range(16)] # La valeur 16 est arbitraire (elle doit seulement être supérieure à 8)
    C = sorted(C, key = lambda l: l[1]) # On range cette liste par distance
    for k in range(16,len(L[0])):
        for l in range(16):
            d = distance(xM, yM, zM, L[5][k], L[3][k], L[4][k])
            if d < C[l][1]:
                C.insert(l,[k,d])
                C.pop()
                break
    C = C[0:8]
    return -moyenne(L,C,xM,yM,zM)
