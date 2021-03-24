#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 14:10:47 2020

@author: Samy Belteton
"""
import tkinter as tk
from tkinter import filedialog 
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "Arial"
font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 8}
matplotlib.rc('font', **font)

root = tk.Tk()
root.withdraw()
print("Select XY coordinates for initial time-point: ")
ini = pd.read_csv(filedialog.askopenfile(),delimiter='\t', header=None)
root.update()
print("Select XY coordinates for last time-point: ")
end = pd.read_csv(filedialog.askopenfile(),delimiter='\t', header=None)
root.update()
print("Select output folder: ")
out = filedialog.askdirectory()

Yi = np.array(-ini[1])
Xi = np.array(ini[0])
Yf = np.array(-end[1])
Xf = np.array(end[0])
oXi = Xi-Xi[0]
oYi = Yi-Yi[0]
oXf = Xf-Xf[0]
oYf = Yf-Yf[0]
radi = - np.arctan(oYi[-1]/oXi[-1])
radf = - np.arctan(oYf[-1]/oXf[-1])
rXi = oXi*np.cos(radi)-oYi*np.sin(radi)
rYi = oXi*np.sin(radi)+oYi*np.cos(radi)
rXf = oXf*np.cos(radf)-oYf*np.sin(radf)
rYf = oXf*np.sin(radf)+oYf*np.cos(radf)
cXi = rXi.mean(axis=0)
cYi = rYi.mean(axis=0)
cXf = rXf.mean(axis=0)
cYf = rYf.mean(axis=0)

# Below for normal comparison
d2Ci = []
d2Cf = []

for i in range(0,np.size(rXi,0),1):
    d2Ci.append(np.abs(np.sqrt((cXi-rXi[i])**2+(cYi-rYi[i])**2)))
    
for i in range(0,np.size(rXf,0),1):
    d2Cf.append(np.abs(np.sqrt((cXf-rXf[i])**2+(cYf-rYf[i])**2)))  

fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(rXi,rYi,'g--')
ax1.plot(cXi,cYi,'go')
ax1.plot(rXf,rYf,'m-')
ax1.plot(cXf,cYf,'mo')
ax2.plot(rXi,d2Ci,'g--')
ax2.plot(rXf,d2Cf,'m-')
ax2.plot(cXi,0,'go')
ax2.plot(cXf,0,'mo')
# Rename the next line for comparison
fig.savefig(os.path.join(out, 'iso_step1-vs-step2.pdf'))

# Below for anisotropic patch. change indexes as necessary
def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

nXi = NormalizeData(rXi)
nXf = NormalizeData(rXf)
cNXi = nXi.mean(axis=0)
cNXf = nXf.mean(axis=0)

d2CNi = []
d2CNf = []

for i in range(0,np.size(nXi,0),1):
    d2CNi.append(np.abs(np.sqrt((cNXi-nXi[i])**2+(cYi-rYi[i])**2)))
    
for i in range(0,np.size(nXf,0),1):
    d2CNf.append(np.abs(np.sqrt((cNXf-nXf[i])**2+(cYf-rYf[i])**2)))  

fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(nXi,rYi,'g--')
ax1.plot(cNXi,cYi,'go')
ax1.plot(nXf,rYf,'m-')
ax1.plot(cNXf,cYf,'mo')
ax2.plot(nXi,d2CNi,'g--')
ax2.plot(nXf,d2CNf,'m-')
ax2.plot(cNXi,0,'go')
ax2.plot(cNXf,0,'mo')
# Rename the next line for comparison
fig.savefig(os.path.join(out, 'ani_step1-vs-step2.pdf'))

fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(nXi,rYi,'palegreen')
ax1.plot(cNXi,cYi,'go')
ax1.plot(nXf[0:19],rYf[0:19],'plum')
ax1.plot(nXf[19:25],rYf[19:25],'grey')
ax1.plot(nXf[25:-1],rYf[25:-1],'plum')
ax1.plot(cNXf,cYf,'mo')
ax2.plot(nXi,d2CNi,'palegreen')
ax2.plot(nXf[0:19],d2CNf[0:19],'plum')
ax2.plot(nXf[19:25],d2CNf[19:25],'grey')
ax2.plot(nXf[25:-1],d2CNf[25:-1],'plum')
#ax2.plot(cXi,0,'go')
#ax2.plot(cXf,0,'mo')
plt.show()
# Rename the next line for comparison
fig.savefig(os.path.join(out, 'step2_iso-vs-ani.pdf'))

fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(nXi[0:19],rYi[0:19],'palegreen')
ax1.plot(nXi[19:25],rYi[19:25],'paleturquoise')
ax1.plot(nXi[25:-1],rYi[25:-1],'palegreen')
ax1.plot(cNXi,cYi,'go')
ax1.plot(nXf[0:19],rYf[0:19],'plum')
ax1.plot(nXf[19:25],rYf[19:25],'moccasin')
ax1.plot(nXf[25:-1],rYf[25:-1],'plum')
ax1.plot(cNXf,cYf,'mo')
ax2.plot(nXi[0:19],d2CNi[0:19],'palegreen')
ax2.plot(nXi[19:25],d2CNi[19:25],'paleturquoise')
ax2.plot(nXi[25:-1],d2CNi[25:-1],'palegreen')
ax2.plot(nXf[0:19],d2CNf[0:19],'plum')
ax2.plot(nXf[19:25],d2CNf[19:25],'moccasin')
ax2.plot(nXf[25:-1],d2CNf[25:-1],'plum')
#ax2.plot(cXi,0,'go')
#ax2.plot(cXf,0,'mo')
plt.show()
# Rename the next line for comparison
fig.savefig(os.path.join(out, 'ani_step1-vs-step2.pdf'))

# This is for quick plotting of rotated shape and distance to center of mass
root = tk.Tk()
root.withdraw()
outputFolder = filedialog.askdirectory()
root.update()

xyCoord_csvFile = filedialog.askopenfile()
root.update()
timepoint = os.path.basename(xyCoord_csvFile.name)[-7:-4]
xyCoord = pd.read_csv(xyCoord_csvFile,delimiter='\t', header=None)
Y = np.array(-xyCoord[1])
X = np.array(xyCoord[0])
X_origin = X-X[0]
Y_origin = Y-Y[0]
radi = - np.arctan(Y_origin[-1]/X_origin[-1])
rotated_X = X_origin*np.cos(radi)-Y_origin*np.sin(radi)
rotated_Y = X_origin*np.sin(radi)+Y_origin*np.cos(radi)
centerOfMass_X = rotated_X.mean(axis=0)
centerOfMass_Y = rotated_Y.mean(axis=0)
distance2CenterOfMass = []
for i in range(0,np.size(rotated_X,0),1):
    distance2CenterOfMass.append(np.abs(np.sqrt(
        (centerOfMass_X-rotated_X[i])**2+
        (centerOfMass_Y-rotated_Y[i])**2)))
plt.scatter(rotated_X,rotated_Y)
plt.ylim([-5,5])
plt.savefig(os.path.join(outputFolder,timepoint+'_segment.pdf'))
plt.show()
plt.scatter(rotated_X,distance2CenterOfMass)
plt.ylim([-1,13])
plt.savefig(os.path.join(
    outputFolder,timepoint+'_distanceToCenterOfMass.pdf'))
rotatedSeg = pd.DataFrame({'x': rotated_X,
                           'y': rotated_Y},
                          index=None)
dist2Center = pd.DataFrame({'x': rotated_X,
                            'dist2Center': distance2CenterOfMass},
                           index=None)
rotatedSeg.to_csv(os.path.join(outputFolder,timepoint+'_rotatedXY.csv'),
                  index = False)
dist2Center.to_csv(os.path.join(outputFolder,timepoint+'_dist2Center.csv'),
                  index = False)