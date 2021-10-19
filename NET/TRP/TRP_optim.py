
from sys import argv
import pandas as pd
import numpy as np
from os import path
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from deap import base, creator, algorithms, tools
import pickle as pkl
import TRP_gaFun as ga


(EXP_FNAME, TRAPS_NUM) = (argv[1], int(argv[2]))
# (EXP_FNAME, TRAPS_NUM) = ('002', 2)
(PT_DTA, PT_IMG) = (
    '/home/chipdelmal/Documents/WorkSims/Mov/dta',
    '/home/chipdelmal/Documents/WorkSims/Mov/trp'
)
kPars = {
    'Trap': {'A': 0.5, 'b': 1},
    'Escape': {'A': 0, 'b': 100}
}
###############################################################################
# GA Settings
############################################################################### 
(POP_SIZE, GENS) = (25, 100)
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
toolbox.register(
    "evaluate", ga.calcFitness, 
    sites=sites, psi=migMat, kPars=kPars, fitFuns=(np.max, np.mean)
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
    pop, toolbox, cxpb=0.5, mutpb=0.25, ngen=GENS, 
    stats=stats, halloffame=hof, verbose=True
)
###############################################################################
# Get Results
############################################################################### 
pklPath = path.join(
    PT_IMG, '{}_{}-GA'.format(EXP_FNAME, str(TRAPS_NUM).zfill(2))
)
(maxFits, meanFits, bestIndx, minFits, traps) = logbook.select(
    "max", "avg", "best", "min", "traps"
)
outList = [
    i for i in zip(minFits, meanFits, maxFits, [list(j) for j in traps])
]
outDF = pd.DataFrame(outList, columns=['min', 'mean', 'max', 'traps'])
outDF.to_csv(pklPath+'.csv', index=False)
with open(pklPath+'.pkl', "wb") as file:
    pkl.dump(outDF, file)
###############################################################################
# Plot landscape
###############################################################################
best = pop[bestIndx[0]]
trapsLocs = list(np.array_split(best, len(best)/2))
BBN = migMat[:sitesNum, :sitesNum]
BQN = migMat[:sitesNum, sitesNum:]
(LW, ALPHA, SCA) = (.125, .5, 50)
(fig, ax) = plt.subplots(figsize=(15, 15))
plt.scatter(
    sites.T[0], sites.T[1], 
    marker='^', color='#03045eDB', 
    s=250, zorder=20, edgecolors='w', linewidths=2
)
for trap in trapsLocs:
    plt.scatter(
        trap[0], trap[1], 
        marker="X", color='#f72585EE', s=1000, zorder=20,
        edgecolors='w', linewidths=2
    )
plt.tick_params(
    axis='both', which='both',
    bottom=False, top=False, left=False, right=False,
    labelbottom=False, labeltop=False, labelleft=False, labelright=False
)
ax.patch.set_facecolor('white')
ax.patch.set_alpha(0)
ax.set_aspect('equal')
ax.set_xlim(minX-.1, maxX+.1)
ax.set_ylim(minY-.1, maxY+.1)
fig.savefig(
    path.join(
        PT_IMG, 
        '{}_{}-GA-trapsNetwork.png'.format(EXP_FNAME, str(TRAPS_NUM).zfill(2))
    ), 
    dpi=250, bbox_inches='tight', transparent=True
)
plt.close()