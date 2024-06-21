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
  
with open(r"C:\Users\marku\Desktop\Code\2024-06-18 16-21-39 KE input beam profile.csv",'r') as csvfile: 
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
popt, pcov = curve_fit(P, positions, powers, bounds=([3,110,-1000,0],[5,130,1000,5]))

positions_fit = np.linspace(positions[0],positions[-1],100)

w_opt = popt[3]
spot_size = 0.707*w_opt

plt.scatter(positions,powers)
plt.plot(positions_fit, P(positions_fit, *popt), 'r-', label='fit: x_half=%5.3f, P_max=%5.3f, P_off=%5.3f, w=%5.3f' % tuple(popt))
plt.xlabel("Position (mm)")
plt.ylabel("Power (mW)")
plt.title("1/e^2 = {:.4f}mm".format(spot_size))
plt.legend()
plt.show()

