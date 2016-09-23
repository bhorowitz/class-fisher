import sys
import numpy as np
import os

# The Crappy Class Interface: CCI
# Ben Horowitz 09/22/16

path_to_class = '/global/homes/b/bhorowit/class_versions/class_public/'
temp_file_name = 'temp.ini'

defaults = {'format':'class','output':'tCl,pCl'}

def run_class(params):
    f = open(temp_file_name, 'w')
    for i in params.keys():
        if isinstance(params[i],list):
            f.write(i+" = " + str(params[i])[1:-1] + "\n")
        else:
            f.write(i+" = " + str(params[i]) + "\n")
    for i in defaults.keys():
        f.write(i+" = " + str(defaults[i]) + "\n") 
    command = path_to_class+"class " + temp_file_name
    print command
    f.close()
    os.system(command)
    data = np.genfromtxt("./output/"+temp_file_name[:-4]+"00_cl.dat")
    os.system("rm ./output/"+temp_file_name[:-4]+"00_cl.dat")
    return data