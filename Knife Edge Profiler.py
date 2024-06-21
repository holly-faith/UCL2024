# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 18:03:43 2024

@author: holly
"""
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import os
import csv
from scipy.special import erf
from scipy.optimize import curve_fit

# Knife edge beam profiler
ready = 0

while ready == 0:
    # define 0 position
    zeropos = float(input("Current micrometer 0 position (mm):"))
    
    # define end position
    endpos = float(input("Desired micrometer end position (mm):"))
    
    # define gaps between measurements
    increment = float(input("Desired increment size (microns):"))
    increment_mm = increment*10**(-3)
    positions = np.arange(zeropos,endpos+increment_mm,increment_mm)
    print(positions)
    
    # confirm or start over
    ready = int(input("You will measure the range {}mm to {}mm with discrete spacing {}microns, this will require {} measurements. Type 1 to confirm or 0 to start over:".format(zeropos, endpos, increment, positions.size)))

print("Starting measurement...")

current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
filename = " ".join([current_datetime,"KE input beam profile.csv"])
print(filename)

powers = []
for pos in positions:
    power = float(input("Power (mW) at position {}mm:".format(pos)))
    powers.append(power)
    
print("Measurement finished. Generating fit. Data is saved as .csv to {}".format)

a = np.array([positions,powers])
filepath = os.path.join(r"C:\Users\marku\Desktop\Code",filename)

with open(filepath, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    csvwriter.writerow(['Position (mm)', 'Power (mW)'])
    
    for position, power in zip(positions, powers):
        csvwriter.writerow([position, power])

# plot raw data as scatter plot
plt.scatter(positions,powers)
plt.xlabel("Position (mm)")
plt.ylabel("Power (mW)")
plt.show()

# ---------------
def P(x, x_half, P_max, P_off, w):
    return P_off + (P_max/2) * erf((x - x_half) / (w / np.sqrt(2)))
# ---------------

# fit data to curve above
popt, pcov = curve_fit(P, positions, powers, bounds=([3,110,-1000,0],[5,130,1000,5]))

positions_fit = np.linspace(positions[0],positions[-1],100)

w_opt = popt[3]

plt.scatter(positions,powers)
plt.plot(positions_fit, P(positions_fit, *popt), 'r-', label='fit: x_half=%5.3f, P_max=%5.3f, P_off=%5.3f, w=%5.3f' % tuple(popt))
plt.xlabel("Position (mm)")
plt.ylabel("Power (mW)")
plt.legend()
plt.show()






