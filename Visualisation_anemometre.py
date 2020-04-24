import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from windrose import WindroseAxes

#ouverture document en mode lecture
f=open("/Users/annegagneux/Desktop/SEMESTRE2/COV_Meteo/Projet_recherche/Depot/Work/1510301.I55","r")


text=f.readlines()
text=text[0].split('\r')
print(len(text))
U=list()
V=list()
W=list()

N=len(text)
for i in range(1,N):
    ligne=text[i]
    ls=ligne.split(',')
    U.append(int(ls[0]))
    V.append(int(ls[1]))
    W.append(int(ls[2]))
    
U=np.array(U)
V=np.array(V)
W=np.array(W)

# composantes de vitesse :
# U= de l'ouest vers l'est
# V = du sud au nord
# W = de bas en haut


#tracé des vitesses
T=np.linspace(0,3600,36000)
plt.plot(T,U,'r')
plt.plot(T,V,'g')
plt.plot(T,W,'b')

def norme(x,y):
    return np.sqrt(x**2+y**2)
    
norm_horizontales=norme(U,V) 


#on visualise le vecteur de coordonnes (-U,-V) car U positif, le vent vient d'Ouest donc il vient de la gauche ce qui correspond à x négatif, de même pour V
 
U_norm=-U/norm_horizontales
V_norm=-V/norm_horizontales
plt.plot(0,0,'r+')
plt.plot(U_norm,V_norm,'+')
plt.show()


#on associe un vecteur vitesse aux composantes U et V-> on affiche ces points sur une carte pour savoir d'où proviennent les vents. L'échelle de couleur donne la vitesse du vent (norme du vecteur (U,V))
def theta(x,y):
    return np.arccos(x/norme(x,y)) #ici arccos bijectif car tm dans cadre sup

theta=theta(U,V)
cm = plt.cm.get_cmap('Spectral')
ax = plt.subplot(111, projection='polar')
sc=ax.scatter(theta,norm_horizontales,c=norm_horizontales,cmap=cm)
plt.colorbar(sc)
plt.show()


#on essaie de créer une rose des vents: on compte la densité de vents qui proviennent de chaque direction (N,N-E,E, etc) en découpant un cercle en différents quartiers. 
comptage=np.zeros(18)
triage=[[] for k in range(18)]

theta_deg=theta*180.0/np.pi
v_max=np.max(norm_horizontales)
for i in range(1,N-1):
    for k in range(0,18):
        if theta_deg[i]<(k+1)*10 and theta_deg[i]>k*10:
            comptage[k]+=1
            
            triage[k].append((theta_deg[i],norm_horizontales[i]))
    
densite=comptage/N
print(densite*100)



#windrose"à la main" sans la valeur des vitesses
t=np.array([10*k for k in range(0,18)])
t=np.pi*t/180.0
ax = plt.subplot(111, projection='polar')
width = np.pi * 18
ax.set_thetagrids(angles=np.arange(0, 360, 45), labels=["E", "N-E", "N", "N-W", "W", "S-W", "S", "S-E"])
ax.bar(t, densite*100,width=0.15)
plt.show()


#windrose
ax = WindroseAxes.from_ax()
ax.bar( theta_deg-90,norm_horizontales, normed=True, opening=0.6 )
ax.set_legend()
plt.show()









