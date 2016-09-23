from copy import *
from math import *
from cci import *
import numpy as np

T_cmb = 2.725

#Planck 2015 Cosmology, for reference/debuging
pfc = {
"omega_b":0.02226,
"omega_cdm": 0.1193,
"h" : 0.6751,
"tau_reio" : 0.063, 
"n_s" :  0.9653,
"A_s" :  2.13e-9 
}

#Planck Experiment Characteristics, defaults, can be easily over-riden

f_sky = 0.65 #originally forcasted for ~.80
weight = 40*10**(-9)/T_cmb #unitless, for P bands: 56
beamsize = 7 #in degrees

def dC_dx(params, x, c_l, p_change=0.001):
    if x not in params:
        raise NameError(x+ " not in parameter list.")
    temp_params = deepcopy(params)
    #c_l = run_class(temp_params) commented out since it will be faster to just calculate this once
    if isinstance(params[x],list):
        temp_params[x]= [i*(1+p_change) for i in params[x]]
        dx = i*(p_change)
    else:
        temp_params[x]= params[x]*(1+p_change)
        dx = params[x]*(p_change)
    c_lp = run_class(temp_params)
    return np.hstack([np.array([c_lp[:,0]]).T,np.divide(c_lp[:,1:]-c_l[:,1:],dx)])

def delta_Cl(l,C_l,f_sky=f_sky,b=beamsize,w=weight):
    B = np.exp(l*(l+1)*b**2/(8*log(2)))
    dC = 2/(f_sky*(2*l+1))*((C_l + w**2*B**(-2))**2)
    return dC

def simple_fisher(params,params_var = [0], p_change = 0.00005,f_sky=f_sky, weight=weight, beamsize=beamsize, verbose=True):
    size = len(params_var)
    if params_var == [0]:
        params_var = params
        size = len(params.keys())
    C=run_class(params)
    F = np.zeros([size,size])
    for i1,j1 in enumerate(params_var):
        for i2,j2 in enumerate(params_var):
            sum_ol = 0
            V1 = dC_dx(params,j1,C,p_change = p_change)
            V2 = dC_dx(params,j2,C,p_change = p_change)
            for l,X in enumerate(C):
                V_deltaC = 1/delta_Cl(X[0],X[1],f_sky=f_sky,b=beamsize,w=weight)
                #print X[0],V_deltaC, V1[l][1],V2[l][1]
                sum_ol = sum_ol + V1[l][1]*V2[l][1]*V_deltaC
            if verbose:
                print j1,j2, sum_ol
            F[i1,i2]=sum_ol
    return F
