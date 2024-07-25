# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:29:31 2024

@author: holly
"""

import matplotlib.pyplot as plt 
import csv 
import math
from scipy.optimize import curve_fit
import numpy as np
from scipy.special import erf
  
positions = [] 
powers = [] 
  
with open(r"C:\Users\marku\Desktop\Code\beam profile data\2024-07-18 14-30-48 KE expanded beam profile.csv",'r') as csvfile: 
    lines = csv.reader(csvfile, delimiter=',') 
    next(lines)
    for row in lines: 
        positions.append(float(row[0])) 
        powers.append(float(row[1])) 
  

# Plot raw data as scatter plot
plt.scatter(positions, powers)  
plt.xlabel('Position (mm)') 
plt.ylabel('Power (mW)')   
plt.show()

# ---------------
def P(x, x_half, P_max, P_off, w):
    return P_off + (P_max/2) * erf((x - x_half) / (w / np.sqrt(2)))
# ---------------

# fit data to curve above
popt, pcov = curve_fit(P, positions, powers, bounds=([0,0,-1000,0],[25,130,1000,20]))

positions_fit = np.linspace(positions[0],positions[-1],100)


w_opt = popt[3]


plt.scatter(positions,powers)
plt.plot(positions_fit, P(positions_fit, *popt), 'r-', label='fit: x_half=%5.3f, P_max=%5.3f, P_off=%5.3f, w=%5.3f' % tuple(popt))
plt.xlabel("Position (mm)")
plt.ylabel("Power (mW)")
plt.legend()
plt.show()

