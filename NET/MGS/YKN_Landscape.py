#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import pandas as pd
from os import path
from sys import argv
from copy import deepcopy
import cartopy.crs as crs
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from compress_pickle import dump, load
from deap import base, creator, algorithms, tools
import MGSurvE as srv
import warnings
warnings.filterwarnings('ignore', 'The iteration is not making good progress')


(LND_PTH, OUT_PTH, ID, EXP) = (
    '/RAID5/marshallShare/MGSurvE_Yorkeys/LandOriginal/Yorkeys03.csv',
    '/RAID5/marshallShare/MGSurvE_Yorkeys/', 
    'YKT', '001'
)
GENS = 2000
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
# YK_LL = YK_LL.reindex(columns=['lat', 'lon'])
# Movement Kernel -------------------------------------------------------------
mKer = {
    'kernelFunction': srv.zeroInflatedExponentialKernel,
    'kernelParams': {'params': srv.AEDES_EXP_PARAMS, 'zeroInflation': 0}
}
###############################################################################
# Defining Traps
###############################################################################
TRPS_NUM = 6
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
        'params': {'A': 1.0, 'rate': 0.1, 'x0': 40}
    },
    0: {
        'kernel': srv.exponentialAttractiveness,
        'params': {'A': 1, 'k': .025, 's': .2, 'gamma': .8, 'epsilon': 0}
    }
}
###############################################################################
# Setting Landscape Up
###############################################################################
lnd = srv.Landscape(
    YK_LL, 
    kernelFunction=mKer['kernelFunction'], kernelParams=mKer['kernelParams'],
    traps=traps, trapsKernels=tKer, trapsRadii=[.5, .6, .75],
    landLimits=YK_BBOX
)
bbox = lnd.getBoundingBox()
trpMsk = srv.genFixedTrapsMask(lnd.trapsFixed)
###############################################################################
# Plot Landscape
###############################################################################
(fig, ax) = (plt.figure(figsize=(15, 15)), plt.axes(projection=crs.PlateCarree()))
lnd.plotSites(fig, ax, size=75)
# lnd.plotMigrationNetwork(
#     fig, ax, 
#     lineWidth=25, alphaMin=.05, alphaAmplitude=2,
# )
# lnd.plotTraps(fig, ax, zorders=(30, 25))
srv.plotClean(fig, ax, bbox=YK_BBOX)
fig.savefig(
    path.join(OUT_PTH, '{}{}_CLN.png'.format(OUT_PTH, ID, TRPS_NUM)), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
plt.close('all')
###############################################################################
# GA Settings
############################################################################### 
POP_SIZE = int(15*(lnd.trapsNumber*1.25))
(MAT, MUT, SEL) = (
    {'mate': .35, 'cxpb': 0.5}, 
    {
        'mean': 0, 
        'sd': min([abs(i[1]-i[0]) for i in bbox])/2.5, 
        'mutpb': .4, 'ipb': .5
    },
    {'tSize': 5}
)
VERBOSE = True
lndGA = deepcopy(lnd)
###############################################################################
# Registering GA functions
############################################################################### 
toolbox = base.Toolbox()
creator.create("FitnessMin", 
    base.Fitness, weights=(-1.0, )
)
creator.create("Individual", 
    list, fitness=creator.FitnessMin
)
toolbox.register("initChromosome", srv.initChromosome, 
    trapsCoords=lndGA.trapsCoords, 
    fixedTrapsMask=trpMsk, coordsRange=bbox
)
toolbox.register("individualCreator", tools.initIterate, 
    creator.Individual, toolbox.initChromosome
)
toolbox.register("populationCreator", tools.initRepeat, 
    list, toolbox.individualCreator
)
# Mate and mutate -------------------------------------------------------------
toolbox.register(
    "mate", tools.cxBlend, 
    alpha=MAT['mate']
)
toolbox.register(
    "mutate", tools.mutGaussian, 
    mu=MUT['mean'], sigma=MUT['sd'], indpb=MUT['ipb']
)
# Select and evaluate ---------------------------------------------------------
toolbox.register("select", 
    tools.selTournament, tournsize=SEL['tSize']
)
toolbox.register("evaluate", 
    srv.calcFitness, 
    landscape=lndGA,
    optimFunction=srv.getDaysTillTrapped,
    optimFunctionArgs={'outer': np.mean, 'inner': np.mean}
)
###############################################################################
# Registering GA stats
############################################################################### 
pop = toolbox.populationCreator(n=POP_SIZE)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)   
stats.register("min", np.min)
stats.register("avg", np.mean)
stats.register("max", np.max)
stats.register("best", lambda fitnessValues: fitnessValues.index(min(fitnessValues)))
stats.register("traps", lambda fitnessValues: pop[fitnessValues.index(min(fitnessValues))])
###############################################################################
# Optimization Cycle
############################################################################### 
(pop, logbook) = algorithms.eaSimple(
    pop, toolbox, cxpb=MAT['cxpb'], mutpb=MUT['mutpb'], ngen=GENS, 
    stats=stats, halloffame=hof, verbose=VERBOSE
)
###############################################################################
# Get and Export Results
############################################################################### 
bestChromosome = hof[0]
bestTraps = np.reshape(bestChromosome, (-1, 2))
dta = pd.DataFrame(logbook)
srv.exportLog(logbook, OUT_PTH, '{}_{:02d}_LOG'.format(ID, TRPS_NUM))
lnd.updateTrapsCoords(bestTraps)
###############################################################################
# Plot Landscape
###############################################################################
(fig, ax) = (plt.figure(figsize=(15, 15)), plt.axes(projection=crs.PlateCarree()))
lnd.plotSites(fig, ax, size=50)
# lnd.plotMigrationNetwork(fig, ax, lineWidth=500, alphaMin=.1, alphaAmplitude=20)
lnd.plotTraps(fig, ax, zorders=(30, 25))
srv.plotFitness(fig, ax, min(dta['min']), fmt='{:.5f}', fontSize=100)
srv.plotClean(fig, ax, bbox=YK_BBOX)
fig.savefig(
    path.join(OUT_PTH, '{}{}_{:02d}_TRP.png'.format(OUT_PTH, ID, TRPS_NUM)), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
plt.close('all')
###############################################################################
# Dump Landscape
###############################################################################
srv.dumpLandscape(lnd, OUT_PTH, '{}_{:02d}_TRP'.format(ID, TRPS_NUM), fExt='pkl')
