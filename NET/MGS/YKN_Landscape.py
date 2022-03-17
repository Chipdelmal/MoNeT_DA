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
    '/home/chipdelmal/Documents/WorkSims/MGSurvE_Yorkeys/LandOriginal/Yorkeys02.csv',
    '/home/chipdelmal/Documents/WorkSims/MGSurvE_Yorkeys/', 
    'YK2', '001'
)
GENS = 10
###############################################################################
# Load pointset
###############################################################################
YK_LL = pd.read_csv(LND_PTH, names=['x', 'y'])
YK_LL['t'] = [0]*YK_LL.shape[0]
pad = 0.00125
YK_BBOX = (
    (min(YK_LL['x'])-pad, max(YK_LL['x'])+pad),
    (min(YK_LL['y'])-pad, max(YK_LL['y'])+pad)
)
# YK_CNTR = [i[0]+(i[1]-i[0])/2 for i in YK_LL]
# SAO_LIMITS = ((6.41, 6.79), (-0.0475, .45))
# Movement Kernel -------------------------------------------------------------
mKer = {
    'kernelFunction': srv.zeroInflatedExponentialKernel,
    'kernelParams': {'params': srv.AEDES_EXP_PARAMS, 'zeroInflation': .1}
}
###############################################################################
# Defining Traps
###############################################################################
TRPS_NUM = 10
nullTraps = [0]*TRPS_NUM
traps = pd.DataFrame({
    'x': [np.mean(YK_LL['x'])]*TRPS_NUM, 'y': [np.mean(YK_LL['y'])]*TRPS_NUM,
    't': [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], 'f': nullTraps
})
tKer = {
    0: {'kernel': srv.exponentialDecay, 'params': {'A': .5, 'b': 1300}},
    1: {'kernel': srv.exponentialDecay, 'params': {'A': .25, 'b': 1300}},
}
###############################################################################
# Setting Landscape Up
###############################################################################
lnd = srv.Landscape(
    YK_LL, 
    kernelFunction=mKer['kernelFunction'], kernelParams=mKer['kernelParams'],
    traps=traps, trapsKernels=tKer,
    landLimits=YK_BBOX
)
bbox = lnd.getBoundingBox()
trpMsk = srv.genFixedTrapsMask(lnd.trapsFixed)
###############################################################################
# Plot Landscape
###############################################################################
(fig, ax) = (plt.figure(figsize=(15, 15)), plt.axes(projection=crs.PlateCarree()))
lnd.plotSites(fig, ax, size=75)
# lnd.plotMigrationNetwork(fig, ax, lineWidth=500, alphaMin=.1, alphaAmplitude=20)
lnd.plotTraps(fig, ax)
srv.plotClean(fig, ax, bbox=YK_BBOX)
fig.savefig(
    path.join(OUT_PTH, '{}{}_CLN.png'.format(OUT_PTH, ID, TRPS_NUM)), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
plt.close('all')
###############################################################################
# GA Settings
############################################################################### 
POP_SIZE = int(10*(lnd.trapsNumber*1.25))
(MAT, MUT, SEL) = (
    {'mate': .35, 'cxpb': 0.5}, 
    {
        'mean': 0, 
        'sd': min([abs(i[1]-i[0]) for i in bbox])/5, 
        'mutpb': .35, 'ipb': .5
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
    optimFunctionArgs={'outer': np.mean, 'inner': np.max}
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
lnd.updateTrapsCoords(bestTraps)
srv.dumpLandscape(lnd, OUT_PTH, '{}_{:02d}_TRP'.format(ID, TRPS_NUM))
dta = pd.DataFrame(logbook)
srv.exportLog(logbook, OUT_PTH, '{}_{:02d}_LOG'.format(ID, TRPS_NUM))
###############################################################################
# Plot Landscape
###############################################################################
(fig, ax) = (plt.figure(figsize=(15, 15)), plt.axes(projection=crs.PlateCarree()))
lnd.plotSites(fig, ax, size=75)
# lnd.plotMigrationNetwork(fig, ax, lineWidth=500, alphaMin=.1, alphaAmplitude=20)
lnd.plotTraps(fig, ax, zorders=(30, 25))
srv.plotClean(fig, ax, bbox=YK_BBOX)
fig.savefig(
    path.join(OUT_PTH, '{}{}_TRP.png'.format(OUT_PTH, ID, TRPS_NUM)), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
plt.close('all')