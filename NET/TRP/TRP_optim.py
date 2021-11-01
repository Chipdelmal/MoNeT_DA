
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
ax.set_ylim(0, 5*minFits[-1])
ax.set_aspect((1/3)/ax.get_data_ratio())
pthSave = path.join(
    PT_GA, '{}_{}-GA.png'.format(EXP_FNAME, str(TRAPS_NUM).zfill(2))
)
fig.savefig(
    pthSave, dpi=aux.DPI, bbox_inches='tight', pad_inches=0, transparent=False
)
plt.close('all')
###############################################################################
# Plot landscape
###############################################################################
best = hof[0]
# Assemble migration with traps -----------------------------------------------
trapsLocs = list(np.array_split(best, len(best)/2))
trapDists = fun.calcTrapToSitesDistance(trapsLocs, sites)
tProbs = fun.calcTrapsSections(trapDists, params=kPars)
tauN = fun.assembleTrapMigration(migMat, tProbs)
BBN = tauN[:sitesNum, :sitesNum]
BQN = tauN[:sitesNum, sitesNum:]
(tpPrs, tRan) = (kPars['Trap'], [.25, .1, .05, .01])
radii = [math.log(tpPrs['A']/y)/(tpPrs['b']) for y in tRan]
# Plot ------------------------------------------------------------------------
(LW, ALPHA, SCA) = (.125, .5, 50)
(fig, ax) = plt.subplots(figsize=(15, 15))
# Traps and sites -------------------------------------------------------------
for trap in trapsLocs:
    plt.scatter(
        trap[0], trap[1], 
        marker="X", color='#f72585FA', s=600, zorder=25,
        edgecolors='w', linewidths=2
    )
    for r in radii:
        circle = plt.Circle(
            (trap[0], trap[1]), r, 
            color='#f7258509', fill=True, ls=':', lw=0, zorder=0
        )
        ax.add_patch(circle)
for (i, site) in enumerate(sites):
    plt.scatter(
        site[0], site[1], 
        marker=aux.MKRS[int(pTypes[i])], color=aux.MCOL[int(pTypes[i])], 
        s=200, zorder=20, edgecolors='w', linewidths=2
    )
# Traps network ---------------------------------------------------------------   
(fig, ax) = aux.plotNetwork(
    fig, ax, BQN*SCA, 
    np.asarray(trapsLocs), sites, 
    [0], c='#d81159', lw=LW*2, alpha=ALPHA*2
)
# Axes ------------------------------------------------------------------------
plt.tick_params(
    axis='both', which='both',
    bottom=False, top=False, left=False, right=False,
    labelbottom=False, labeltop=False, labelleft=False, labelright=False
)
ax.text(
    0.5, 0.5, '{:.2f}'.format(minFits[-1]),
    horizontalalignment='center', verticalalignment='center',
    fontsize=100, color='#00000011',
    transform=ax.transAxes, zorder=5
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
background.save(pthSave, dpi=(aux.DPI, aux.DPI))
background.close()
foreground.close()
