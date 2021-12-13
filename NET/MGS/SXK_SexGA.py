#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import pandas as pd
from os import path
from sys import argv
from copy import deepcopy
import matplotlib.pyplot as plt
from compress_pickle import dump, load
from deap import base, creator, algorithms, tools
import MGSurvE as srv
import warnings
warnings.filterwarnings('ignore', 'The iteration is not making good progress')


(GENS, VERBOSE) = (750, True)
if srv.isNotebook():
    (OUT_PTH, LND_TYPE, ID, OPT_TYPE) = (
        '/home/chipdelmal/Documents/WorkSims/MGSurvE_Benchmarks/SX_BENCH/', 
        'UNIF', 'SX1', 'M'
    )
else:
    (OUT_PTH, LND_TYPE, ID, OPT_TYPE) = (
        argv[1], argv[2], argv[3].zfill(3), argv[4]
    )
###############################################################################
# Internals
###############################################################################
TRPS_NUM=3
ID="{}-{:03d}".format(ID, TRPS_NUM)
if OPT_TYPE == 'M':
    (weightMale, weightFemale) = (1, 0)
elif OPT_TYPE == 'F':
    (weightMale, weightFemale) = (0, 1)
else:
    (weightMale, weightFemale) = (.75, 1)
###############################################################################
# Load Landscape
###############################################################################
lndM = srv.loadLandscape(OUT_PTH, '{}_{}_M_CLN'.format(LND_TYPE, ID))
lndF = srv.loadLandscape(OUT_PTH, '{}_{}_F_CLN'.format(LND_TYPE, ID))
# Needed auxiliary variables --------------------------------------------------
bbox = lndM.getBoundingBox()
trpMsk = srv.genFixedTrapsMask(lndM.trapsFixed)
ID="{}-{}".format(ID, OPT_TYPE)
###############################################################################
# GA Settings
############################################################################### 
POP_SIZE = int(10*(lndM.trapsNumber*1.25))
(MAT, MUT, SEL) = (
    {'mate': .3, 'cxpb': 0.5}, 
    {'mean': 0, 'sd': min([i[1]-i[0] for i in bbox])/5, 'mutpb': .4, 'ipb': .5},
    {'tSize': 3}
)
lndM_GA = deepcopy(lndM)
lndF_GA = deepcopy(lndF)
###############################################################################
# Registering Functions for GA
############################################################################### 
toolbox = base.Toolbox()
creator.create("FitnessMin", 
    base.Fitness, weights=(-1.0, )
)
creator.create("Individual", 
    list, fitness=creator.FitnessMin
)
toolbox.register("initChromosome", srv.initChromosome, 
    trapsCoords=lndM_GA.trapsCoords, 
    fixedTrapsMask=trpMsk, coordsRange=bbox
)
toolbox.register("individualCreator", tools.initIterate, 
    creator.Individual, toolbox.initChromosome
)
toolbox.register("populationCreator", tools.initRepeat, 
    list, toolbox.individualCreator
)
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
    srv.calcSexFitness, 
    landscapeMale=lndM_GA,landscapeFemale=lndF_GA,
    weightMale=.75, weightFemale=1,
    optimFunction=srv.getDaysTillTrapped,
    optimFunctionArgs={'outer': np.mean, 'inner': np.max}
)
###############################################################################
# Registering functions for GA stats
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
# Update with best results ----------------------------------------------------
minFits= logbook.select("min")
lndM.updateTrapsCoords(np.reshape(hof[0], (-1, 2)))
lndF.updateTrapsCoords(np.reshape(hof[0], (-1, 2)))
srv.dumpLandscape(lndM, OUT_PTH, '{}_{}_M_TRP'.format(LND_TYPE, ID))
srv.dumpLandscape(lndF, OUT_PTH, '{}_{}_F_TRP'.format(LND_TYPE, ID))
dta = pd.DataFrame(logbook)
srv.exportLog(logbook, OUT_PTH, '{}_{}_LOG'.format(LND_TYPE, ID))
###############################################################################
# Plot traps
############################################################################### 
# (fig, ax) = plt.subplots(1, 1, figsize=(15, 15), sharey=False)
lndF.plotTraps(fig, ax, colors={0: '#f7258522'}, lws=(2, 0), fill=True, ls='--', zorder=(25, 4))
lndM.plotTraps(fig, ax, colors={0: '#ffffffDD'}, lws=(2, 2), fill=False, zorder=(-5, 5))
srv.plotClean(fig, ax, frame=False, bbox=bbox)
# srv.plotFitness(fig, ax, min(minFits))
fig.savefig(
    path.join(OUT_PTH, '{}_{}_TRP.png'.format(LND_TYPE, ID)), 
    facecolor='w', bbox_inches='tight', pad_inches=0, dpi=300
)
plt.close('all')
###############################################################################
# Plot GA
############################################################################### 
(fig, ax) = plt.subplots(figsize=(15, 15))
(fig, ax) = srv.plotGAEvolution(fig, ax, dta)
# srv.plotClean(fig, ax)
pthSave = path.join(
    OUT_PTH, '{}_{}_GAP'.format(LND_TYPE, ID)
)
fig.savefig(
    pthSave,
    facecolor='w', bbox_inches='tight', pad_inches=.1, dpi=300
)
