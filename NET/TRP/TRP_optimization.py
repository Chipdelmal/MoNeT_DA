
import math
import numpy as np
from os import path
from sys import argv
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from deap import base, creator, algorithms, tools
import TRP_aux as aux
import TRP_fun as fun
import TRP_gaFun as ga

TRAPS_NUM = 4
(PT_DTA, PT_IMG, EXP_FNAME) = (
    '/home/chipdelmal/Documents/WorkSims/Mov/dta',
    '/Volumes/marshallShare/Mov/trp/Benchmark',
    '100'
)
POP_SIZE = 100
kPars = {
    'Trap': {'A': 0.5, 'b': 1},
    'Escape': {'A': 0, 'b': 100}
}

###############################################################################
# Read migration matrix and pop sites
############################################################################### 
pthBase = path.join(PT_DTA, EXP_FNAME)
migMat = np.genfromtxt(pthBase+'_MX.csv', delimiter=',')
sites = np.genfromtxt(pthBase+'_XY.csv', delimiter=',')
# Sites and landscape shapes --------------------------------------------------
sitesNum = sites.shape[0]
(minX, minY) = np.apply_along_axis(min, 0, sites)
(maxX, maxY) = np.apply_along_axis(max, 0, sites)
(xMinMax, yMinMax) = ((minX, maxX), (minY, maxY))
###############################################################################
# Registering functions for GA
############################################################################### 
toolbox = base.Toolbox()
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
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
toolbox.register("mate", tools.cxUniform, indpb=0.25)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
# toolbox.register('evaluate', ga.calculateFitness, CLS_SET=CLS_SET, COM_SET=COM_SET)
toolbox.register(
    "evaluate", ga.calcFitness, 
    sites=sites, psi=migMat, kPars=kPars
)
###############################################################################
# Init Population
############################################################################### 
population = toolbox.populationCreator(n=POP_SIZE)