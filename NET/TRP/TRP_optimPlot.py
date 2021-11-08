
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
    (EXP_FNAME, TRAPS_NUM) = ('LRG_01-350-HOM', 5)
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths('lab')
else:
    (EXP_FNAME, TRAPS_NUM) = (argv[1], int(argv[2]))
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths(argv[3])
kPars = aux.KPARS
print('* Plotting: {} (traps={})'.format(EXP_FNAME, TRAPS_NUM))
bgImg = '{}_BF.png'.format(EXP_FNAME)
pklPath = path.join(
    PT_GA, '{}_{}_GA'.format(EXP_FNAME, str(TRAPS_NUM).zfill(2))
)
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
# Read GA data ----------------------------------------------------------------
with open(pklPath+'.pkl', "rb") as file:
    ga = pkl.load(file)
cols = [ga['max'], ga['mean'], ga['min'], ga['traps']]
(maxFits, meanFits, minFits, traps) = [list(i) for i in cols]
(bestVal, bestIx) = min((val, idx) for (idx, val) in enumerate(minFits))
best = ga['traps'].iloc[bestIx]
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
(fig, ax) = aux.plotTraps(
    fig, ax, trapsLocs, bestVal, sites, pTypes, radii, BQN,
    minX, minY, maxX, maxY
)
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