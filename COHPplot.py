#Program to plot the most significant COHP interactions from COHPCAR.lobster

import numpy as np
import scipy as sp
import re
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib import rc, ticker

def importData(filename,spin_polar):  #generic function to read in data
#returns list of ineraction names, array of energy range, array of average/integrated, and array of
#actual values.  This final array is 3D if spin-polar

    f = open(filename, 'r')
    line = f.readline() #Skip title line

    s = f.readline().split()  #how many interactions?
    numInteractions = int(s[0])-1
    nedos = int(s[2]) #number of points in energy scale
    
    line = f.readline() #Skip Average

    Interactions = []
    energyScale = np.zeros([nedos])
    avgInt = np.zeros([nedos,2*spin_polar])
    values = np.zeros([nedos,2*numInteractions*spin_polar])

    interactionCount = 0
    while interactionCount < numInteractions:  #Fill the list with interaction titles
        Interactions.append(f.readline())

        interactionCount += 1

    for i in range(0,nedos):
        s = f.readline().split()
        energyScale[i] = s[0]
        avgInt[i,0:2] = s[1:3]
        values[i,0:2*numInteractions] = s[3:3+2*numInteractions]

        if spin_polar == 2:
            avgInt[i,2:4] = s[3+2*numInteractions:5+2*numInteractions]
            values[i,2*numInteractions:] = s[5+2*numInteractions:]

    return Interactions, energyScale, avgInt, values

temp = importData(str('C:/Users/Steven/Documents/Oxynit_COHP/YSn_COHPCAR.lobster'),2)

for i in range(0,len(temp[0])):
    print(i,end="",flush=True)
    print(temp[0][i],end="",flush=True)
    print(np.trapz(abs(temp[3][:,i*2]),x=temp[1]))
    print()

def plotCOHP(data, indices, title=''):  #takes as input the data from the COHPCAR.lobster, and the indices
    # of the interaction
    if title == '':
        title = data[0][indices[0]][0:30]
    sum = np.sum([data[3][:,i*2] for i in indices], axis=0)
    plot = plt.plot(data[1],sum, lw=2)
    plt.plot(data[1],np.sum([data[3][:,i*2 + 1] for i in indices],axis=0),color='r', lw=2)
    plt.tick_params(axis='both',which='major',labelsize=32)
    plt.title(title,fontsize=18)
    plt.xlim((-1,3))
    plt.ylim((-0.05,0.05))
    plt.xlabel(r'E - E$_F$ (eV)', fontsize=26)
    plt.ylabel('COHP', fontsize = 26)
    plt.axvline(x=0)
    plt.tight_layout()
    plt.show()

plotCOHP(temp, [30])
#[1,4],r'Cu 4$s$ / O 2$s$,2$p$'
# [0], r'Cu / O Total'
