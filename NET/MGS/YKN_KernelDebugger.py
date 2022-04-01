#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import pandas as pd
from os import path
from copy import deepcopy
import cartopy.crs as crs
import matplotlib.pyplot as plt
from compress_pickle import dump, load
from itertools import chain

import MGSurvE as srv
import warnings
warnings.filterwarnings('ignore', 'The iteration is not making good progress')


(LND_PTH, OUT_PTH, ID, EXP) = (
    '/RAID5/marshallShare/MGSurvE_Yorkeys/LandOriginal/Yorkeys02.csv',
    '/RAID5/marshallShare/MGSurvE_Yorkeys/Debug/', 
    'YKD', '001'
)
###############################################################################
# Load pointset
###############################################################################
YK_LL = pd.read_csv(LND_PTH, names=['lon', 'lat'])
YK_LL['t'] = [0]*YK_LL.shape[0]
pad = 0.00125
YK_BBOX = (
    (min(YK_LL['lon'])-pad, max(YK_LL['lon'])+pad),
    (min(YK_LL['lat'])-pad, max(YK_LL['lat'])+pad)
)
center = [np.mean(i) for i in YK_BBOX]
range = [(i[1]-i[0])/2 for i in YK_BBOX]
# YK_LL = YK_LL.reindex(columns=['lat', 'lon'])
# Movement Kernel -------------------------------------------------------------
mKer = {
    'kernelFunction': srv.zeroInflatedExponentialKernel,
    'kernelParams': {'params': srv.AEDES_EXP_PARAMS, 'zeroInflation': 0}
}
###############################################################################
# Defining Traps
###############################################################################
TRPS_NUM = 1
nullTraps = [0]*TRPS_NUM
traps = pd.DataFrame({
    'lon': [np.mean(YK_LL['lon'])]*TRPS_NUM, 
    'lat': [np.mean(YK_LL['lat'])]*TRPS_NUM,
    't': [0]*TRPS_NUM, 'f': nullTraps
})
tKer = {
    2: {
        'kernel': srv.exponentialDecay, 
        'params': {'A': .5, 'b': 0.1}
    },
    1: {
        'kernel': srv.sigmoidDecay,     
        'params': {'A': .5, 'rate': 0.25, 'x0': 10}
    },
    0: {
        'kernel': srv.exponentialAttractiveness,
        'params': {'A': 1, 'k': .025, 's': .2, 'gamma': .8, 'epsilon': 0}
    }
}
# Set landscape up ------------------------------------------------------------
lnd = srv.Landscape(
    YK_LL, 
    kernelFunction=mKer['kernelFunction'], kernelParams=mKer['kernelParams'],
    traps=traps, trapsKernels=tKer, trapsRadii=[.5, .6, .75],
    landLimits=YK_BBOX
)
###############################################################################
# Setup traps 
###############################################################################
ptRans = ((-0.1, 0.75), )
bestTraps = [(range[0]*ptRan[0]+center[0], range[1]*ptRan[1]+center[1]) for ptRan in ptRans]
pos = list(chain(*bestTraps))
###############################################################################
# Calculate position
###############################################################################
fitness = srv.calcFitness(
    pos, lnd,
    optimFunction=srv.getDaysTillTrapped,
    optimFunctionArgs={'outer': np.mean, 'inner': np.mean}
)
lnd.updateTrapsCoords(bestTraps)
bbox = lnd.getBoundingBox()
###############################################################################
# Plot Landscape
###############################################################################
(fig, ax) = (plt.figure(figsize=(15, 15)), plt.axes(projection=crs.PlateCarree()))
lnd.plotSites(fig, ax, size=50)
lnd.plotTraps(fig, ax, zorders=(30, 25))
srv.plotFitness(fig, ax, fitness[0], fmt='{:.5f}', fontSize=100)
srv.plotClean(fig, ax, bbox=YK_BBOX)
fig.savefig(
    path.join(OUT_PTH, '{}{}_{:02d}_{}_TRP.png'.format(
        OUT_PTH, ID, TRPS_NUM, [int(i*100) for i in ptRans[0]])
    ), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
plt.close('all')
