##Plots=group
##showplots
##Layer=vector
##X=Field Layer

import matplotlib.pyplot as plt
f=[]
for i in Layer[[X]]:
    f.append(i)
plt.plot(f)
plt.ylabel('some numbers')
plt.show()