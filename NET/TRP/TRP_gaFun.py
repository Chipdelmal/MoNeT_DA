
import copy
from os import path
import numpy as np
import numpy.random as rand
import TRP_fun as fun

# (PT_DTA, EXP_FNAME) = (
#     '/home/chipdelmal/Documents/WorkSims/Mov/dta',
#     #'/Volumes/marshallShare/Mov/dta',
#     '002'
# )
# pth = path.join(PT_DTA, EXP_FNAME)
# migMat = np.genfromtxt(pth+'_MX.csv', delimiter=',')
# sites = np.genfromtxt(pth+'_XY.csv', delimiter=',')

###############################################################################
# Initialization
###############################################################################
def initChromosome(trapsNum, xRan, yRan):
    xCoords = np.random.uniform(xRan[0], xRan[1], trapsNum)
    yCoords = np.random.uniform(yRan[0], yRan[1], trapsNum)
    chromosome = [val for pair in zip(xCoords, yCoords) for val in pair]
    return chromosome

###############################################################################
# Mutation and Crossover
###############################################################################
def mutateChromosome(
        chromosome, 
        randFun=rand.normal, randArgs={'loc': 0, 'scale': 0.1}
    ):
    randDraw = randFun(size=len(chromosome), **randArgs)
    mutChrom = chromosome + randDraw
    return mutChrom

###############################################################################
# Fitness
###############################################################################
def calcFitness(
        chromosome, 
        sites=[[0, 0]], psi=[[1]], 
        kPars={'Trap': {'A': 0.5, 'b': 1}, 'Escape': {'A': 0, 'b': 100}}, 
        fitFuns=(np.max, np.mean)
    ):
    # Calc required vars (pre-compute for speed) ------------------------------
    dims = 2
    (sitesN, trapsN) = (int(sites.shape[0]), int(len(chromosome)/dims))
    traps = np.asarray(np.array_split(chromosome, len(chromosome)/dims))
    # Calculate migration matrix with traps -----------------------------------
    trapDists = fun.calcTrapToSitesDistance(traps, sites)
    tProbs = fun.calcTrapsSections(trapDists, params=kPars)
    tauN = fun.assembleTrapMigration(psi, tProbs)
    # Re-assemble in canonical form -------------------------------------------
    tauCan = fun.reshapeInCanonicalForm(tauN, sitesN, trapsN)
    F = fun.getMarkovAbsorbing(tauCan, trapsN)
    # Calculate fitness -------------------------------------------------------
    daysTillTrapped = np.apply_along_axis(fitFuns[0], 1, F)
    fitness = fitFuns[1](daysTillTrapped)
    return [float(abs(fitness))]

