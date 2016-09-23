#Displays marginalized values from CLASS
from simple_fisher import *
F_planck = simple_fisher(pfc)
inverse = np.linalg.inv(F_planck)
print "Marginalized values for parameter errrors are:"
for i,_ in enumerate(F_planck):
    print pfc.keys()[i], 2*sqrt(inverse[i,i])