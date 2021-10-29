
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
from PIL import Image

if monet.isNotebook():
    (EXP_FNAME, TRAPS_NUM) = ('BASE-100-HOM', 1)
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths('dsk')
else:
    (EXP_FNAME, TRAPS_NUM) = (argv[1], int(argv[2]))
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths(argv[3])
kPars = aux.KPARS
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
     sites = sites[:, 0:2]
(minX, minY) = np.apply_along_axis(min, 0, sites)
(maxX, maxY) = np.apply_along_axis(max, 0, sites)
(xMinMax, yMinMax) = ((minX, maxX), (minY, maxY))
###############################################################################
# GA Settings
############################################################################### 
(POP_SIZE, GENS) = (20, 1000)
(MATE, MUTATE, SELECT) = (
    {'mate': .3, 'cxpb': 0.5}, 
    {'mean': 0, 'sd': (maxX-minX)/5, 'ipb': .5, 'mutpb': .3},
    {'tSize': 3}
)
VERBOSE = True
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
    pop, toolbox, cxpb=MATE['cxpb'], mutpb=MUTATE['mutpb'], ngen=GENS, 
    stats=stats, halloffame=hof, verbose=VERBOSE
)
###############################################################################
# Get Results
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
###############################################################################
# Plot GA
###############################################################################
x = range(len(minFits))    
(fig, ax) = plt.subplots(figsize=(15, 15))
# plt.plot(x, maxFits, color='#00000000')
plt.plot(x, meanFits, lw=.5, color='#ffffffFF')
# plt.plot(x, minFits, ls='dotted', lw=2.5, color='#f72585')
ax.fill_between(x, maxFits, minFits, alpha=0.9, color='#1565c077')
ax.set_xlim(0, max(x))
ax.set_ylim(0, 5*max(meanFits))
ax.set_aspect((1/3)/ax.get_data_ratio())
pthSave = path.join(
    PT_GA, '{}_{}-GA.png'.format(EXP_FNAME, str(TRAPS_NUM).zfill(2))
)
fig.savefig(
    pthSave, dpi=aux.DPI, bbox_inches='tight', 
    pad_inches=0, transparent=True
)
plt.close('all')
###############################################################################
# Plot landscape
###############################################################################
best = hof[0]
trapsLocs = list(np.array_split(best, len(best)/2))
BBN = migMat[:sitesNum, :sitesNum]
BQN = migMat[:sitesNum, sitesNum:]
(LW, ALPHA, SCA) = (.125, .5, 50)
(fig, ax) = plt.subplots(figsize=(15, 15))
for trap in trapsLocs:
    plt.scatter(
        trap[0], trap[1], 
        marker="X", color='#f72585EE', s=500, zorder=20,
        edgecolors='w', linewidths=2
    )
plt.tick_params(
    axis='both', which='both',
    bottom=False, top=False, left=False, right=False,
    labelbottom=False, labeltop=False, labelleft=False, labelright=False
)
ax.text(
    0.5, 0.5, '{:.2f}'.format(minFits[-1]),
    horizontalalignment='center', verticalalignment='center',
    fontsize=100, color='#00000011',
    transform=ax.transAxes, zorder=50
)
ax.patch.set_facecolor('white')
ax.patch.set_alpha(0)
ax.set_aspect('equal')
ax.set_xlim(minX-aux.PAD, maxX+aux.PAD)
ax.set_ylim(minY-aux.PAD, maxY+aux.PAD)
pthSave = path.join(
    PT_IMG, '{}_{}.png'.format(EXP_FNAME, str(TRAPS_NUM).zfill(2))
)
fig.savefig(
    pthSave, dpi=aux.DPI, bbox_inches='tight', 
    pad_inches=0, transparent=True
)
plt.close('all')
###############################################################################
# Overlay Brute-force
###############################################################################
time.sleep(3)
background = Image.open(path.join(PT_IMG, bgImg))
foreground = Image.open(pthSave)
(w, h) = background.size
background = background.crop((0, 0, w, h))
foreground = foreground.resize((int(w/1), int(h/1)),Image.ANTIALIAS)
background.paste(foreground, (0, 0), foreground)
background.save(pthSave)
background.close()
foreground.close()
