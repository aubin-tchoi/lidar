
# cd OneDrive/1A/Lidar

from Parseur import *
from Layout import *

path    = "/Users/aubin/OneDrive/1A/Lidar/Work/"
chemin1 = path + "1510301.I55.txt"
chemin2 = path + "WLS200s-15_radial_wind_data_2015-04-13_01-00-00.csv"


U,V,W = ParseurSonique(chemin1)
L,T   = ParseurLidar(chemin2)

"""
u.er = UsinOcosP + VcosOcosP + WsinP
u(k).er(l) = U[k]T[1][l]T[2][l] + V[k]T[0][k]T[2][l] + W[k]T[3][l]
-> Reste à faire le bon choix de k et l : la discrétisation des deux champs n'est pas la même,
Pour chaque point Lidar, on peut interpoler (linéairement) le champ de vitesses Sonique entre deux points proches
(proches en rho, theta et phi : rho = moyenne quad(x,y,z), theta = arcsin(z/rho), phi = arctan(y/x)
"""

xL,yL = Layout(path,False) # rho, theta et phi sont calculés à partir de cette origine
