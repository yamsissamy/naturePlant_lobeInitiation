#!/anaconda3/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:21:59 2019

@author: Samy Belteton
"""
import tkinter as tk
from tkinter import filedialog 
import os
import glob 
import matplotlib
from matplotlib.ticker import MaxNLocator
#matplotlib.use("TkAgg")
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "Arial"
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy import interpolate
font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 8}

matplotlib.rc('font', **font)

"""
- Import folders set up
- Asks which cell is the initiating cell
  cell1 is on top, cell2 is bottom
"""
#from scipy.signal import find_peaks
root = tk.Tk()
root.withdraw() 
print("Select text image folder:")
txtImg = filedialog.askdirectory() 
root.update()
print("Select output folder:")
outFolder = filedialog.askdirectory()
root.update()
iCell = int(input("Which cell is the initiating cell (1 or 2)? "))
awmFiles = sorted(glob.glob(os.path.join(txtImg, 'AW*.txt')))
if iCell == 1:
    pc1Files = sorted(glob.glob(os.path.join(txtImg, 'C1*.txt')))
    pc2Files = sorted(glob.glob(os.path.join(txtImg, 'C2*.txt')))
else:
    pc1Files = sorted(glob.glob(os.path.join(txtImg, 'C2*.txt')))
    pc2Files = sorted(glob.glob(os.path.join(txtImg, 'C1*.txt')))
    
tTmp = len(awmFiles)
preNormAWM = pd.DataFrame()
preNormOP1 = pd.DataFrame()
preNormOP2 = pd.DataFrame()
posNormAWM = pd.DataFrame()
posNormOP1 = pd.DataFrame()
posNormOP2 = pd.DataFrame()
apexMTEnrich = pd.DataFrame(columns=['tmpt','initApexMTSig','follApexMTSig','initEnrich'])
print("")

"""
- Change saveName to be the the timelapse and lobe of interest
- Will ask the timepoint at which lobe was first detected
- Will ask the location of the lobe at detection
- Will ask the width of the apex at detection

- These values can be obtained from segmentShapePlots.py code by:
    - setting i to the timepoint of lobe detection then running the code after for loop (line 78):
        data = pd.read_csv(i, sep='\t',header=None)
        Y = np.array(-data[1])
        X = np.array(data[0])
        ...
    - Then iPeaks for inverted peaks, otherwise uPeaks for location
    - Then iPeaksHalfWidth for inverted peaks, otherwise uPeaksHalfWidth for lobe apex
"""
saveName = 'MTEnrichmentLGMTPM05Seg1NewLobe1'

for i in awmFiles:
    print(awmFiles.index(i)," = ", i[-7:-4])
preL = int(input("Enter timepoint at which lobe is detected: "))
lLoc = float(input("Enter lobe location at detection: "))*500
hLwd = float(input("Enter lobe initial apex width: "))*250
#fLoc = float(input("Enter lobe location at last timepoint:"))*500
#fLwd = float(input("enter lobe final width:"))*.125
preLAW = awmFiles[:preL]
posLAW = awmFiles[preL:]
preOC1 = pc1Files[:preL]
posOC1 = pc1Files[preL:]
preOC2 = pc2Files[:preL]
posOC2 = pc2Files[preL:]

for i in range(0,preL):
    dfAW = pd.read_csv(preLAW[i],sep='\t',header=None)
    dfC1 = pd.read_csv(preOC1[i],sep='\t',header=None)
    dfC2 = pd.read_csv(preOC2[i],sep='\t',header=None)
    sum_dfAW = dfAW.sum()
    sum_dfC1 = dfC1.sum()
#    if iCell == 1:
#        sum_dfC1 = dfC1.iloc[10:19,:].sum()
#        sum_dfC2 = dfC2.iloc[0:9,:].sum()
#    else:
#        sum_dfC1 = dfC1.iloc[0:9,:].sum()
#        sum_dfC2 = dfC2.iloc[10:19,:].sum()
    sum_dfC2 = dfC2.sum()
    minMT = min(np.min(sum_dfC1),np.min(sum_dfC2))
    maxMT = max(np.max(sum_dfC1),np.max(sum_dfC2))
    norm_dfAW = (sum_dfAW-np.min(sum_dfAW))/(np.max(sum_dfAW)-np.min(sum_dfAW))
    norm_dfC1 = (sum_dfC1-minMT)/(maxMT-minMT)
    norm_dfC2 = (sum_dfC2-minMT)/(maxMT-minMT)
    splineFAW = interpolate.interp1d(np.arange(0,norm_dfAW.size),norm_dfAW)
    splineFC1 = interpolate.interp1d(np.arange(0,norm_dfC1.size),norm_dfC1)
    splineFC2 = interpolate.interp1d(np.arange(0,norm_dfC2.size),norm_dfC2)
    sp_range = np.linspace(0, norm_dfAW.size-1, num=500, endpoint=True)
    preNormAWM[preLAW[i][-6:-4]] = splineFAW(sp_range)
    preNormOP1[preLAW[i][-6:-4]] = splineFC1(sp_range)
    preNormOP2[preLAW[i][-6:-4]] = splineFC2(sp_range)
    
for i in range(preL-preL,tTmp-preL):
    dfAW = pd.read_csv(posLAW[i],sep='\t',header=None)
    dfC1 = pd.read_csv(posOC1[i],sep='\t',header=None)
    dfC2 = pd.read_csv(posOC2[i],sep='\t',header=None)
    sum_dfAW = dfAW.sum()
    sum_dfC1 = dfC1.sum()
#    if iCell == 1:
#        sum_dfC1 = dfC1.iloc[10:19,:].sum()
#        sum_dfC2 = dfC2.iloc[0:9,:].sum()
#    else:
#        sum_dfC1 = dfC1.iloc[0:9,:].sum()
#        sum_dfC2 = dfC2.iloc[10:19,:].sum()

    sum_dfC2 = dfC2.sum()
    minMT = min(np.min(sum_dfC1),np.min(sum_dfC2))
    maxMT = max(np.max(sum_dfC1),np.max(sum_dfC2))
    norm_dfAW = (sum_dfAW-np.min(sum_dfAW))/(np.max(sum_dfAW)-np.min(sum_dfAW))
    #norm_dfC1 = (sum_dfC1-np.min(sum_dfC1))/(np.max(sum_dfC1)-np.min(sum_dfC1))
    #norm_dfC2 = (sum_dfC2-np.min(sum_dfC2))/(np.max(sum_dfC2)-np.min(sum_dfC2))
    norm_dfC1 = (sum_dfC1-minMT)/(maxMT-minMT)
    norm_dfC2 = (sum_dfC2-minMT)/(maxMT-minMT)
    splineFAW = interpolate.interp1d(np.arange(0,norm_dfAW.size),norm_dfAW)
    splineFC1 = interpolate.interp1d(np.arange(0,norm_dfC1.size),norm_dfC1)
    splineFC2 = interpolate.interp1d(np.arange(0,norm_dfC2.size),norm_dfC2)
    sp_range = np.linspace(0, norm_dfAW.size-1, num=500, endpoint=True)
    posNormAWM[posLAW[i][-6:-4]] = splineFAW(sp_range)
    posNormOP1[posLAW[i][-6:-4]] = splineFC1(sp_range)
    posNormOP2[posLAW[i][-6:-4]] = splineFC2(sp_range)

totalAWM = pd.concat([preNormAWM, posNormAWM], axis=1, sort=False)
totalOP1 = pd.concat([preNormOP1, posNormOP1], axis=1, sort=False)
totalOP2 = pd.concat([preNormOP2, posNormOP2], axis=1, sort=False)



# Getting the area at the apex for initial vs following cells
initCellPers = np.sum(preNormOP1, axis = 1)
follCellPers = np.sum(preNormOP2, axis = 1)
apexLimUp = int(np.round(lLoc+hLwd))
apexLimDw = int(np.round(lLoc-hLwd))
trapzInit = np.trapz(initCellPers[apexLimDw:apexLimUp])
trapzFoll = np.trapz(follCellPers[apexLimDw:apexLimUp])
initMTAbund = (trapzInit/trapzFoll-1)*100




fig, allFig = plt.subplots(3,1,sharex = True)
fig.subplots_adjust(hspace = 0)
allFig[0].stackplot(totalAWM.index,totalAWM.values.T,)
allFig[0].axvline(x=lLoc, linewidth=1, ls = ':', c = 'black')
allFig[0].axvline(x=lLoc-hLwd, linewidth=1, ls = ':', c = 'cyan')
allFig[0].axvline(x=lLoc+hLwd, linewidth=1, ls = ':', c = 'cyan')
#allFig[0].set_yticks(np.arange(0.0,tTmp+2,2))
allFig[0].yaxis.set_major_locator(MaxNLocator(5))
allFig[0].set_ylim(-1, tTmp+1)
allFig[0].set_xticks(np.arange(0.0,502,125))
allFig[0].set_xticklabels([0.0,0.25,0.50,0.75,1.0])
allFig[0].annotate('Anticlinal MT', (.01, .9), xycoords='axes fraction', va='center')
allFig[0].annotate('All timepoints', (0, 1.1), xycoords='axes fraction', va='center')
allFig[1].stackplot(totalOP1.index,totalOP1.values.T,)
allFig[1].axvline(x=lLoc, linewidth=1, ls = ':', c = 'black')
allFig[1].axvline(x=lLoc-hLwd, linewidth=1, ls = ':', c = 'cyan')
allFig[1].axvline(x=lLoc+hLwd, linewidth=1, ls = ':', c = 'cyan')
allFig[1].yaxis.set_major_locator(MaxNLocator(5))
allFig[1].set_ylim(-1, tTmp+1)
allFig[1].annotate('Initiating Cell: Outer Peri. MT', (.01, .9), xycoords='axes fraction', va='center')
allFig[2].stackplot(totalOP2.index,totalOP2.values.T,)
allFig[2].axvline(x=lLoc, linewidth=1, ls = ':', c = 'black')
allFig[2].axvline(x=lLoc-hLwd, linewidth=1, ls = ':', c = 'cyan')
allFig[2].axvline(x=lLoc+hLwd, linewidth=1, ls = ':', c = 'cyan')
allFig[2].yaxis.set_major_locator(MaxNLocator(5))
allFig[2].set_ylim(-1, tTmp+1)
allFig[2].annotate('Following Cell: Outer Peri. MT', (.01, .9), xycoords='axes fraction', va='center')
plt.xlabel("Norm. segment length")
fig.text(0.04, 0.5, 'Acumulated MT signal', va='center', rotation='vertical')
fig.savefig(os.path.join(outFolder,'')+'All.pdf')


fig, preFig = plt.subplots(3,1,sharex = True)
fig.subplots_adjust(hspace = 0)
preFig[0].stackplot(preNormAWM.index,preNormAWM.values.T,)
preFig[0].axvline(x=lLoc, linewidth=1, ls = ':', c = 'black')
preFig[0].axvline(x=lLoc-hLwd, linewidth=1, ls = ':', c = 'cyan')
preFig[0].axvline(x=lLoc+hLwd, linewidth=1, ls = ':', c = 'cyan')
preFig[0].yaxis.set_major_locator(MaxNLocator(5))
preFig[0].set_ylim(-1, preL+1)
preFig[0].set_xticks(np.arange(0.0,502,125))
preFig[0].set_xticklabels([0.0,0.25,0.50,0.75,1.0])
preFig[0].annotate('Anticlinal MT', (.01, .9), xycoords='axes fraction', va='center')
preFig[0].annotate('Prior to lobe detection', (0, 1.1), xycoords='axes fraction', va='center')
preFig[0].annotate('Init. cell MT enrichment at apex: %3.0f %%' % initMTAbund , (0.4, 1.1), xycoords='axes fraction', va='center')
preFig[1].stackplot(preNormOP1.index,preNormOP1.values.T,)
preFig[1].axvline(x=lLoc, linewidth=1, ls = ':', c = 'black')
preFig[1].axvline(x=lLoc-hLwd, linewidth=1, ls = ':', c = 'cyan')
preFig[1].axvline(x=lLoc+hLwd, linewidth=1, ls = ':', c = 'cyan')
preFig[1].yaxis.set_major_locator(MaxNLocator(5))
preFig[1].set_ylim(-1, preL+1)
preFig[1].annotate('Initiating Cell: Outer Peri. MT', (.01, .9), xycoords='axes fraction', va='center')
preFig[2].stackplot(preNormOP2.index,preNormOP2.values.T,)
preFig[2].axvline(x=lLoc, linewidth=1, ls = ':', c = 'black')
preFig[2].axvline(x=lLoc-hLwd, linewidth=1, ls = ':', c = 'cyan')
preFig[2].axvline(x=lLoc+hLwd, linewidth=1, ls = ':', c = 'cyan')
preFig[2].yaxis.set_major_locator(MaxNLocator(5))
preFig[2].set_ylim(-1, preL+1)
preFig[2].annotate('Following Cell: Outer Peri. MT', (.01, .9), xycoords='axes fraction', va='center')
plt.xlabel("Norm. segment length")
fig.text(0.04, 0.5, 'Acumulated MT signal', va='center', rotation='vertical')
fig.savefig(os.path.join(outFolder,'')+'preLobe.pdf')

fig, posFig = plt.subplots(3,1,sharex = True)
fig.subplots_adjust(hspace = 0)
posFig[0].stackplot(posNormAWM.index,posNormAWM.values.T,)
posFig[0].axvline(x=lLoc, linewidth=1, ls = ':', c = 'black')
posFig[0].axvline(x=lLoc-hLwd, linewidth=1, ls = ':', c = 'cyan')
posFig[0].axvline(x=lLoc+hLwd, linewidth=1, ls = ':', c = 'cyan')
posFig[0].yaxis.set_major_locator(MaxNLocator(5))
posFig[0].set_ylim(-1, tTmp-preL+1)
posFig[0].set_xticks(np.arange(0.0,502,125))
posFig[0].set_xticklabels([0.0,0.25,0.50,0.75,1.0])
posFig[0].annotate('Anticlinal MT', (.01, .9), xycoords='axes fraction', va='center')
posFig[0].annotate('After lobe detection', (0, 1.1), xycoords='axes fraction', va='center')
posFig[1].stackplot(posNormOP1.index,posNormOP1.values.T,)
posFig[1].axvline(x=lLoc, linewidth=1, ls = ':', c = 'black')
posFig[1].axvline(x=lLoc-hLwd, linewidth=1, ls = ':', c = 'cyan')
posFig[1].axvline(x=lLoc+hLwd, linewidth=1, ls = ':', c = 'cyan')
posFig[1].yaxis.set_major_locator(MaxNLocator(5))
posFig[1].set_ylim(-1, tTmp-preL+1)
posFig[1].annotate('Initiating Cell: Outer Peri. MT', (.01, .9), xycoords='axes fraction', va='center')
posFig[2].stackplot(posNormOP2.index,posNormOP2.values.T,)
posFig[2].axvline(x=lLoc, linewidth=1, ls = ':', c = 'black')
posFig[2].axvline(x=lLoc-hLwd, linewidth=1, ls = ':', c = 'cyan')
posFig[2].axvline(x=lLoc+hLwd, linewidth=1, ls = ':', c = 'cyan')
posFig[2].yaxis.set_major_locator(MaxNLocator(5))
posFig[2].set_ylim(-1, tTmp-preL+1)
posFig[2].annotate('Following Cell: Outer Peri. MT', (.01, .9), xycoords='axes fraction', va='center')
plt.xlabel("Norm. segment length")
fig.text(0.04, 0.5, 'Acuuulated MT signal', va='center', rotation='vertical')
fig.savefig(os.path.join(outFolder,'')+'posLobe.pdf')

antiSum = preNormAWM.sum(axis=1)
initSum = preNormOP1.sum(axis=1)
follSum = preNormOP2.sum(axis=1)


antiSum.to_csv(os.path.join(outFolder,'anticlinalMTSum')+'.csv', header=True)
initSum.to_csv(os.path.join(outFolder,'initCellMTSum')+'.csv', header=True)
follSum.to_csv(os.path.join(outFolder,'FollCellMTSum')+'.csv', header=True)

for i in np.arange(np.size(preNormOP1,axis=1)):
    tOP1=np.trapz(preNormOP1.iloc[:,i][apexLimDw:apexLimUp])
    tOP2=np.trapz(preNormOP2.iloc[:,i][apexLimDw:apexLimUp])
    P1oP2=(tOP1/tOP2-1)*100
    apexMTEnrich = apexMTEnrich.append({'tmpt':preNormOP1.columns[i],
                                        'initApexMTSig':tOP1,
                                        'follApexMTSig':tOP2,
                                        'initEnrich':P1oP2},ignore_index=True)

    
fig, mtEnr = plt.subplots(1,1)
mtEnr.set_title(saveName)
mtEnr.scatter(apexMTEnrich.tmpt,apexMTEnrich.initEnrich, c='m',s=1)
plt.xlabel('Timepoints')
plt.ylabel('Init. MT Enrichment (%)')
plt.xlim(0,23)
plt.xticks(np.arange(4, 24, step=5))
ax2=mtEnr.twinx()
plt.ylabel('Init. MT Enrichment (%)')
plt.tight_layout()
plt.show()
fig.savefig(os.path.join(outFolder,saveName)+'.pdf')

apexMTEnrich.to_csv(os.path.join(outFolder,saveName)+'.csv', header=True, index=False)



"""
- Below if for stress and MT comparison
- This is based on the segment of interest with csv files obtained from Abaqcus  
""" 
stress = pd.read_csv(filedialog.askopenfile())
awSum = pd.read_csv(filedialog.askopenfile(),index_col=0)
c1Sum = pd.read_csv(filedialog.askopenfile(),index_col=0)
c2Sum = pd.read_csv(filedialog.askopenfile(),index_col=0)



stressC1 = stress['C1_ZST']
stressC2 = stress['C2_ZST'][0:27]
norm_StressC1 = (stressC1-np.min(stressC1))/(np.max(stressC1)-np.min(stressC1))
norm_StressC2 = (stressC2-np.min(stressC2))/(np.max(stressC2)-np.min(stressC2))
spln_StressC1 = interpolate.interp1d(np.arange(0,norm_StressC1.size),norm_StressC1)
spln_StressC2 = interpolate.interp1d(np.arange(0,norm_StressC2.size),norm_StressC2)
sp_rangeC1 = np.linspace(0, norm_StressC1.size-1, num=500, endpoint=True)
sp_rangeC2 = np.linspace(0, norm_StressC2.size-1, num=500, endpoint=True)
C1Stress = pd.DataFrame(spln_StressC1(sp_rangeC1))
C2Stress = pd.DataFrame(spln_StressC2(sp_rangeC2))
AWStress = C1Stress+C2Stress

#awSum = preNormAWM.sum(axis=1)
#c1Sum = preNormOP1.sum(axis=1)
#c2Sum = preNormOP2.sum(axis=1)
 

plt.subplot(1, 2, 1)
plot(np.arange(0,500,1),C1Stress, 'b')
plt.subplot(1, 2, 2)
plot(np.arange(0,500,1),c1Sum,'g')
plt.tight_layout()
np.corrcoef(C1Stress,c1Sum)[0,1]

plt.subplot(1, 2, 1)
plot(np.arange(0,500,1),C2Stress, 'b')
plt.subplot(1, 2, 2)
plot(np.arange(0,500,1),c2Sum,'g')
plt.tight_layout()
np.corrcoef(C2Stress,c2Sum)[0, 1]

plt.subplot(1, 2, 1)
plot(np.arange(0,500,1),AWStress, 'b')
plt.subplot(1, 2, 2)
plot(np.arange(0,500,1),awSum,'g')
plt.tight_layout()
np.corrcoef(AWStress,awSum)[0, 1]

plt.subplot(1, 2, 1)
plot(np.arange(0,500,1),AWStress, 'b')
plt.subplot(1, 2, 2)
plot(np.arange(0,500,1),c1Sum+c2Sum,'g')
plt.tight_layout()
np.corrcoef(AWStress,c1Sum+c2Sum)[0, 1]


for i in np.arange(size(preNormOP1,axis=1)): 
    fig, ax1 = plt.subplots()
    ax1.plot(preNormOP1.iloc[:,i],c='g')
    ax1.plot(preNormOP2.iloc[:,i],c='m')
    plt.show()

