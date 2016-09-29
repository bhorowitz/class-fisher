import sys
import numpy as np
import os

# The Crappy Class Interface: CCI
# Ben Horowitz 09/22/16

#path_to_class = '/global/homes/b/bhorowit/class_versions/class_public/'
temp_file_name = 'temp.ini'
pre_file_name = 'precision.pre'

defaults = {'format':'class','output':'tCl,pCl'}

default_pre = {'l_max_ur':20}


def run_class(params,pre=default_pre, path_to_class='/global/homes/b/bhorowit/class_versions/class_public/'):
    f = open(temp_file_name, 'w')
    p = open(pre_file_name, 'w')
    for i in params.keys():
        if isinstance(params[i],list):
            f.write(i+" = " + str(params[i])[1:-1] + "\n")
        else:
            f.write(i+" = " + str(params[i]) + "\n")
    for i in defaults.keys():
        f.write(i+" = " + str(defaults[i]) + "\n") 
    for i in pre.keys():

        p.write(i+" = " + str(pre[i]) + "\n")
    command = path_to_class+"class " + temp_file_name + " " + pre_file_name + " > class.log"
 
    f.close()
    p.close()
    os.system(command)
    try:
        data = np.genfromtxt("./output/"+temp_file_name[:-4]+"00_cl.dat")
        os.system("rm ./output/*")
    except:
            raise NameError("Error in class, check class.log file")
    return data