# Représentation des points en lesquels on dispose d'une mesure Lidar

from numpy import cos, sin, pi
import seaborn as sns
import matplotlib.pyplot as plt

def Maillage(L,n,s,pause,xL,yL,zL,xM,yM,zM):
    _, (ax1, ax2) = plt.subplots(1, 2, sharex = True)
    ax1.set_title("y,x")
    ax2.set_title("z,x")
    ax1.scatter(xM, yM, s = 2*s, color = 'g', alpha = 0.75)
    ax2.scatter(xM, zM, s = 2*s, color = 'g', alpha = 0.75)
    for i in range(n):
        rho = L[5][i]
        theta = pi*(L[3][i]+180)/180
        phi = pi*L[4][i]/180
        x = rho*sin(theta)*cos(phi) + xL
        y = rho*cos(theta)*cos(phi) + yL
        z = rho*sin(phi) + zL
        ax1.scatter(x, y, s = s, color = 'b', alpha = 0.75)
        ax2.scatter(x, z, s = s, color = 'b', alpha = 0.75)
        plt.pause(pause)