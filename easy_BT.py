# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt

kpoints = np.linspace(-0.5,0.5,1000)
deltae = 0.0005
ene = np.linspace(0,1,int(1/deltae)) #Ry
mu = np.linspace(-0.5, 0.5 , 1000)
hbar = 1
e = 1
#tau = 1e-14 
tau = 1
#Kb = 8.6173303 * 10**-5 / 13.606  #Ry #1Ry = 2Ha
Kb = 8.6173303 * 10**-5
volume = 95.76   #A^3 -> m^3
T = 300 #K
def sig_k(group_v, tau, e):
    return e**2 *tau *group_v **2
def FD_dist(ene, mu, T):
    factor = (ene-mu)/(Kb*T)
    return 1./(np.exp(factor)+1)
def dFD_distdene(ene, mu, T):
    factor = (ene-mu)/(Kb*T)
    if factor > 40 or factor <-40:
        return 0
    else:
        exp = np.exp(factor)
        return -exp/(Kb*T*(exp+1)**2)
def peak_fun(ene, max_x , h,w):
    peak = np.array([])
    for i in ene:
        down_bound = max_x - w
        up_bound =  max_x + w 
        if i > down_bound and i < up_bound:
            peak = np.append(peak, -h/w**2*(i-max_x)**2+h)
            #peak = np.append(peak, 1)
        else:
            peak = np.append(peak, 0)
    return peak
v = 5
c = 5
gap = 0.12 #Ry
sig_e = []
mid = (max(ene)+min(ene))/2
for i in ene:
    if i > mid + gap / 2:
        sig_e.append( c*(i-(mid+gap/2))**2)
    elif i < mid -gap / 2:
        sig_e.append( v*(i-(mid-gap/2))**2)
    else:
        sig_e.append(0)
sig_e = np.array(sig_e)
plt.plot(ene, sig_e)

def get_data_from_files(file = "./sig_e_for_test.xlsx"):
    import xlrd
    aa = xlrd.open_workbook(file)
    sheet1 = aa.sheet_by_index(0)
    ene = sheet1.col_values(0)
    sig_e = sheet1.col_values(1)
    return ene, sig_e
def factor_plot(mu, T):
    factor_sig = np.array([])
    factor_gr = np.array([])
    for i in ene:
        factor_sig = np.append(factor_sig, -dFD_distdene(i, mu,T)) 
        factor_gr = np.append(factor_gr, -dFD_distdene(i, mu,T)* (i-mu))
    plt.plot(ene, factor_gr, label="T= "+str(T))
    return factor_sig, factor_gr
def mu_fun(sig_e, ene, mu, volume = 1):
    sig_mu = np.array([])
    group_mu = np.array([])
    for j in mu:
        factor_sig = np.array([])
        factor_gr = np.array([])
        for i in ene:
            factor_sig = np.append(factor_sig, -dFD_distdene(i, j,T)) 
            factor_gr = np.append(factor_gr, -dFD_distdene(i, j,T)* (j-i))
        tmp_sig_mu = sig_e * factor_sig * deltae
        tmp_sig_mu = tmp_sig_mu.sum() / volume 
        sig_mu = np.append(sig_mu, tmp_sig_mu)
        tmp_group_mu = sig_e * factor_gr  * deltae
        tmp_group_mu = tmp_group_mu.sum() / (volume*T*e) 
        group_mu = np.append(group_mu, tmp_group_mu)
    seeb_mu = group_mu / sig_mu
    PF_mu = seeb_mu**2 * sig_mu
    plt.plot(mu, sig_mu*2.93E20)
    plt.xlabel(r"$\mu$")
    plt.ylabel(r'$\sigma$ / $\tau$ (S/m s)')
    plt.show()
    #plt.plot(mu, seeb_mu*1E6)
    plt.plot(mu, seeb_mu*13*1E6)
    plt.xlabel(r"$\mu$")
    plt.ylabel(r"$S$ $(\mu V/K)$")
    plt.show()
    plt.plot(mu, PF_mu)
    plt.xlabel(r"$\mu$")
    plt.ylabel(r"$PF /\tau$ $(\mu W/mK^2 s)$")

    return sig_mu, group_mu, seeb_mu, PF_mu
def anal_tool(mu, mu_funs):
    Max = mu_funs.argmax()
    Min = mu_funs.argmin()
    print ( ene[Max],max(mu_funs))
    print (ene[Min],min(mu_funs))
#mu_fun(sig_e, ene, mu, volume)
