#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from os import path
from copy import deepcopy
import matplotlib.pyplot as plt
import MGSurvE as srv
import cartopy.crs as ccrs


GENS = 2000
CF_NAME = 'COORDS.csv'
(PTH_O, PTH_I) = ('./out', './in')
###############################################################################
# Load Pointset
###############################################################################
SITES = pd.read_csv(path.join(PTH_I, 'LatLon_Yap.csv'))
SITES['t'] = [0]*SITES.shape[0]
SITES_bbox = (
    (min(SITES['lon']), max(SITES['lon'])),
    (min(SITES['lat']), max(SITES['lat']))
)
SITES_cntr = [i[0]+(i[1]-i[0])/2 for i in SITES_bbox]
###############################################################################
# Movement Kernel
###############################################################################
mKer = {'params':srv.AEDES_EXP_PARAMS, 'zeroInflation': .2}
###############################################################################
# Traps
###############################################################################
traps = pd.DataFrame({
    'lon': [SITES_cntr[0]]*4, 
    'lat': [SITES_cntr[1]]*4, 
    'f': [0, 0, 0, 0],
    't': [0, 0, 0, 1]
})
tKer = {
    0: {'kernel': srv.exponentialDecay, 'params': {'A': 1, 'b': .0075}},
    1: {'kernel': srv.exponentialDecay, 'params': {'A': 1, 'b': .0050}},
}
###############################################################################
# Setting Landscape Up
###############################################################################
lnd = srv.Landscape(
    SITES, # landLimits=SITES_bbox,
    kernelParams=mKer,
    traps=traps, trapsKernels=tKer,
    trapsRadii=[.75, .5, .3],
)
bbox = lnd.getBoundingBox()
trpMsk = srv.genFixedTrapsMask(lnd.trapsFixed)
###############################################################################
# Plot Landscape
###############################################################################
# (fig, ax) = (
#     plt.figure(figsize=(15, 15)),
#     plt.axes(projection=ccrs.PlateCarree())
# )
# lnd.plotSites(fig, ax, size=250)
# lnd.plotTraps(fig, ax)
# srv.plotClean(fig, ax)
# # COMMENT MIGRATION NETWORK OUT IF TAKING TOO LONG! ---------------------------
# lnd.plotMigrationNetwork(
#     fig, ax, lineWidth=60, alphaMin=.1, alphaAmplitude=5,
# )
# # -----------------------------------------------------------------------------
# # lnd.plotLandBoundary(fig, ax)
# srv.plotClean(fig, ax, bbox=lnd.landLimits)
# fig.savefig(
#     path.join(PTH_O, 'Landscape_CLN.png'), 
#     facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
# )
# plt.close('all')
# (fig, ax) = plt.subplots(1, 1, figsize=(15, 15), sharey=False)
# (fig, ax) = srv.plotTrapsKernels(
#     fig, ax, lnd, 
#     colors=srv.MCOL, distRange=(0, 500), aspect=.25
# )
# fig.savefig(
#     path.join(PTH_O, 'TrapKernels.png'), 
#     facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
# )
# plt.close('all')
###############################################################################
# GA Settings (Modify the number of generations!!!)
############################################################################### 
POP_SIZE = int(10*(lnd.trapsNumber*1.25))
(GENS, MAT, MUT, SEL) = (
    100,
    {'mate': .3, 'cxpb': 0.5}, 
    {'mean': 0, 'sd': min([i[1]-i[0] for i in bbox])/5, 'mutpb': .5, 'ipb': .5},
    {'tSize': 4}
)
lndGA = deepcopy(lnd)
###############################################################################
# Running GA Optimization
############################################################################### 
(lnd, logbook) = srv.optimizeTrapsGA(
    lndGA, pop_size='auto', generations=GENS,
    mating_params=MAT, mutation_params=MUT, selection_params=SEL,
    fitFuns={'outer': np.mean, 'inner': np.mean}, verbose=True
)
srv.exportLog(logbook, PTH_O, 'Landscape_LOG')
###############################################################################
# Plot Optimized Landscape
############################################################################### 
(fig, ax) = plt.subplots(1, 1, figsize=(15, 15), sharey=False)
lnd.plotSites(fig, ax, size=100)
lnd.plotMigrationNetwork(fig, ax, alphaMin=.6, lineWidth=25)
lnd.plotTraps(fig, ax)
srv.plotClean(fig, ax, frame=False)
srv.plotFitness(fig, ax, min(logbook['min']))
fig.savefig(
    path.join(PTH_O, 'Landscape_TRP.png'), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
plt.close('all')