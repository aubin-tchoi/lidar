import matplotlib.pyplot as plt
import numpy as np


num_eol=range(1,9)
x_eol=[1013.29,1379.26,1683.97,2009.33,2336.49,2703.76,3236.12,3603.45]
y_eol=[2760.29,2475.197,2222.269,1968.963,1808.297,1585.12,1358.848,1135.73]


x_mat=1472
y_mat=1979


x_lid=1000
y_lid=1000


for n in num_eol:
    plt.plot(x_eol[n-1],y_eol[n-1],'r+')
plt.plot(x_mat,y_mat,'g+')
plt.plot(x_lid,y_lid,'b+')
plt.show()










