# Comparaison des valeurs de vent obtenues

import numpy as np

# Calcul des coordonnées sphériques d'un point désigné par ses coordonnées cartésiennes

def cart_to_pol(x,y,z,xL,yL,zL):
    rho = np.sqrt((x-xL)**2 + (y-yL)**2 + (z-zL)**2)
    theta = np.arctan((y-yL)/(x-xL))*180/np.pi
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

# Renvoit un tuple correspondant aux intervalles entre chaque mesure de r, de theta ou de phi

def Pas(L):
    def quicksort(x):   # C'est vraiment un quicksort
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
    N = len(L[0])
    r, theta, phi = quicksort(L[5]), quicksort(L[3]), quicksort(L[4])
    dr     = min([r[k] - r[k-1] for k in range(2,N)])
    dtheta = min([theta[k] - theta[k-1] for k in range(2,N)])
    dphi   = min([phi[k] - phi[k-1] for k in range(2,N)])
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
    for k in range(n):
        V += L[6][k]
    V = V/n     # Moyenne arithmétique de la vitesse en tous les points de C (
    return V

def Interpolation(L,x,y,z,xL,yL,zL):
    rho, theta, phi = cart_to_pol(x,y,z,xL,yL,zL)
    V = 0
    return V
