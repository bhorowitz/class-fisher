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
        params_var = params #if varying parameters unspecified, vary all given parameters (Note: Doesn't work with discrete parameters)
        size = len(params.keys())
    C=run_class(params) # calculates value at test point
    F = np.zeros([size,size]) #initialized fisher matrix
    for i1,j1 in enumerate(params_var):
        V1 = dC_dx(params,j1,C,p_change = p_change)
        for i2,j2 in enumerate(params_var):
            sum_ol = 0
            print j1, j2
            V2 = dC_dx(params,j2,C,p_change = p_change)
            for l,model in enumerate(C):
                for X in range(0,3):
                    for Y in range(0,3):
                        #Currently only TT power spectrum fisher model working properly.
                        if (X ==0 and Y==0): #TT, TT
                            V_deltaC = 1/delta_Cl(model[0],model[1],f_sky=f_sky,b=beamsize,w=weight)
                        else if (X==0 and Y==1) or (X==1 and Y==0): #TT, EE
                             V_deltaC = 0
                        else if (X==0 and Y==2) or (X==2 and Y==0): #TT, TE
                             V_deltaC = 0
                        else if (X==1 and Y==1): #EE,EE
                            V_deltaC = 0 #1/delta_Cl(model[0],model[1+X],w=56*10**(-9)/T_cmb)
                        else if (X==1 and Y==2) or (X==2 and Y==1): #TE,EE
                            V_deltaC = 0
                        else if (X==2 and Y==2): #TE, TE
                            V_deltaC = 0 #1/delta_Cl(model[0],model[1+X],w=0)
                        else:
                            raise NameError("Channel doesn't exist!")
                        sum_ol = sum_ol + V1[l][1+X]*V2[l][1+Y]*V_deltaC
            if verbose:
                print j1,j2, sum_ol
            F[i1,i2]=sum_ol
    return F
