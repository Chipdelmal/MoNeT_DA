
import time
import math
from sys import argv
import pandas as pd
import numpy as np
from os import path
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from deap import base, creator, algorithms, tools
import pickle as pkl
import TRP_gaFun as ga
import TRP_aux as aux
import TRP_fun as fun
from PIL import Image

if monet.isNotebook():
    (EXP_FNAME, TRAPS_NUM) = ('SQR_01-150-HOM', 1)
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths('lab')
else:
    (EXP_FNAME, TRAPS_NUM) = (argv[1], int(argv[2]))
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths(argv[3])
(kPars, GENS) = (aux.KPARS, 1000)
print('* Optimizing: {} (traps={})'.format(EXP_FNAME, TRAPS_NUM))
bgImg = '{}_BF.png'.format(EXP_FNAME)
###############################################################################
# Read migration matrix and pop sites
############################################################################### 
pthBase = path.join(PT_DTA, EXP_FNAME)
migMat = np.genfromtxt(pthBase+'_MX.csv', delimiter=',')
sites = np.genfromtxt(pthBase+'_XY.csv', delimiter=',')
# Sites and landscape shapes --------------------------------------------------
sitesNum = sites.shape[0]
if sites.shape[1] > 2:
    pTypes = sites[:,2]
    sites = sites[:, 0:2]
(minX, minY) = np.apply_along_axis(min, 0, sites)
(maxX, maxY) = np.apply_along_axis(max, 0, sites)
(xMinMax, yMinMax) = ((minX, maxX), (minY, maxY))
###############################################################################
# GA Settings
############################################################################### 
POP_SIZE = int(10*(TRAPS_NUM*1.25))
(MATE, MUTATE, SELECT) = (
    {'mate': .3, 'cxpb': 0.5}, 
    {'mean': 0, 'sd': (maxX-minX)/5, 'ipb': .5, 'mutpb': .3},
    {'tSize': 3}
)
VERBOSE = False
###############################################################################
# Registering functions for GA
############################################################################### 
toolbox = base.Toolbox()
creator.create("FitnessMin", base.Fitness, weights=(-1.0, ))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox.register(
    "initChromosome", ga.initChromosome, 
    trapsNum=TRAPS_NUM, xRan=xMinMax, yRan=yMinMax
)
toolbox.register(
    "individualCreator", tools.initIterate, 
    creator.Individual, toolbox.initChromosome
)
toolbox.register(
    "populationCreator", tools.initRepeat, 
    list, toolbox.individualCreator
)
toolbox.register(
    "mate", tools.cxBlend, 
    alpha=MATE['mate']
)
toolbox.register(
    "mutate", tools.mutGaussian, 
    mu=MUTATE['mean'], sigma=MUTATE['sd'], indpb=MUTATE['ipb']
)
toolbox.register(
    "select", tools.selTournament, 
    tournsize=SELECT['tSize']
)
toolbox.register(
    "evaluate", ga.calcFitness, 
    sites=sites, psi=migMat, kPars=kPars, fitFuns=(np.mean, np.mean)
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
# Running GA
############################################################################### 
(pop, logbook) = algorithms.eaSimple(
    pop, toolbox, cxpb=MATE['cxpb'], mutpb=MUTATE['mutpb'], ngen=GENS, 
    stats=stats, halloffame=hof, verbose=VERBOSE
)
###############################################################################
# Get and Export Results
############################################################################### 
(maxFits, meanFits, bestIndx, minFits, traps) = logbook.select(
    "max", "avg", "best", "min", "traps"
)
pklPath = path.join(
    PT_GA, '{}_{}_GA'.format(EXP_FNAME, str(TRAPS_NUM).zfill(2))
)
outList = [
    i for i in zip(minFits, meanFits, maxFits, [list(j) for j in traps])
]
outDF = pd.DataFrame(outList, columns=['min', 'mean', 'max', 'traps'])
outDF.to_csv(pklPath+'.csv', index=False)
with open(pklPath+'.pkl', "wb") as file:
    pkl.dump(outDF, file)

