##[Plots]=group
##layer=vector
##Ratiofield=field layer
##GoogleRatio=field layer
#Sukhjit Singh Sehra v1.0 created on 5-02-17 used to create a demo single variable plot

from qgis.core import *
from PyQt4.QtCore import *
import numpy as np
import matplotlib.pyplot as plt

inlayer = processing.getObject(layer)
ratiofielddict=[]
Gratiofielddict=[]
for f in inlayer.getFeatures():
    ratiofielddict.append(f[Ratiofield])

for f in inlayer.getFeatures():
    Gratiofielddict.append(f[GoogleRatio])

#For converting dict to array 
x = np.array(ratiofielddict)
y = np.array(Gratiofielddict)



plt.plot(x)
plt.plot(y)

plt.show()