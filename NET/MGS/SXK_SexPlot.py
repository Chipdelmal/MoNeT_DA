#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from os import path
from sys import argv
import matplotlib.pyplot as plt
from compress_pickle import dump, load
import MGSurvE as srv


(GENS, VERBOSE) = (500, False)
if srv.isNotebook():
    (OUT_PTH, LND_TYPE, ID, TRPS_NUM, OPT_TYPE) = (
        '/home/chipdelmal/Documents/WorkSims/MGSurvE_Benchmarks/SX_BENCH/', 
        'UNIF', 'SX1', 6, 'M'
    )
else:
    (OUT_PTH, LND_TYPE, ID, TRPS_NUM, OPT_TYPE) = (
        argv[1], argv[2], argv[3].zfill(3), int(argv[4]), argv[5]
    )
###############################################################################
# Internals
###############################################################################
ID="{}-{:03d}".format(ID, TRPS_NUM)
if OPT_TYPE == 'M':
    (weightMale, weightFemale) = (1, 0)
elif OPT_TYPE == 'F':
    (weightMale, weightFemale) = (0, 1)
else:
    (weightMale, weightFemale) = (.5, 1)
###############################################################################
# Load Data
############################################################################### 
lndM = srv.loadLandscape(OUT_PTH, '{}_{}_M_CLN'.format(LND_TYPE, ID))
lndF = srv.loadLandscape(OUT_PTH, '{}_{}_F_CLN'.format(LND_TYPE, ID))
ID="{}-{}".format(ID, OPT_TYPE)
dat = srv.importLog(OUT_PTH, '{}_{}_LOG'.format(LND_TYPE, ID))
# Getting stats ---------------------------------------------------------------
(gaMin, gaTraps, gens) = (list(dat['min']), dat['traps'], dat.shape[0])
bbox = lndM.getBoundingBox()
ix = gaMin.index(min(gaMin))
trapsCoords = np.reshape(
    np.fromstring(gaTraps[ix][1:-1], sep=','), (-1, 2)
).T
trapsLocs = pd.DataFrame(
    np.vstack([trapsCoords, lndM.trapsTypes, lndM.trapsFixed]).T, 
    columns=['x', 'y', 't', 'f']
)
lndMU = lndM.updateTraps(trapsLocs, lndM.trapsKernels)
lndFU = lndF.updateTraps(trapsLocs, lndF.trapsKernels)
###############################################################################
# Plot traps
############################################################################### 
(fig, ax) = plt.subplots(1, 1, figsize=(15, 15), sharey=False)
lndM.plotSites(fig, ax, size=100)
# Plot Networks ---------------------------------------------------------------
if (OPT_TYPE=='M' or OPT_TYPE=='B'):
    lndM.plotMigrationNetwork(fig, ax, alphaMin=.3, lineWidth=50, lineColor='#03045e')
if (OPT_TYPE=='F' or OPT_TYPE=='B'):
    lndF.plotMigrationNetwork(fig, ax, alphaMin=.3, lineWidth=35, lineColor='#03045e')
# Plot Traps ------------------------------------------------------------------
if OPT_TYPE=='M':
    lndM.plotTraps(fig, ax, colors={0: '#a06cd522'}, lws=(2, 0), fill=True, ls=':', zorder=(25, 4))
if OPT_TYPE=='F':
    lndF.plotTraps(fig, ax, colors={0: '#f7258522'}, lws=(2, 0), fill=True, ls='--', zorder=(25, 4))
if OPT_TYPE=='B':
    lndF.plotTraps(fig, ax, colors={0: '#f7258522'}, lws=(2, 0), fill=True, ls='--', zorder=(25, 4))
    lndM.plotTraps(fig, ax, colors={0: '#a06cd522'}, lws=(2, 0), fill=True, ls=':', zorder=(25, 4))
    # lndM.plotTraps(fig, ax, colors={0: '#ffffffDD'}, lws=(2, 2), fill=True, ls=':', zorder=(26, 5))
# Other Stuff -----------------------------------------------------------------
srv.plotFitness(fig, ax, min(gaMin), zorder=30)
srv.plotClean(fig, ax, frame=True, bbox=bbox, labels=False)
fig.savefig(
    path.join(OUT_PTH, '{}_{}_TRP.png'.format(LND_TYPE, ID)), 
    facecolor='w', bbox_inches='tight', pad_inches=0.05, dpi=300
)
plt.close('all')
