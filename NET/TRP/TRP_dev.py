
import math
import numpy as np
from os import path
from sys import argv
import networkx as nx
# import cdlib.algorithms as cd
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
import TRP_aux as aux
import TRP_fun as fun

TRAPS_NUM = 3
(PT_DTA, PT_IMG, EXP_FNAME) = (
    '/Volumes/marshallShare/Mov/dta',
    '/Volumes/marshallShare/Mov/trp/Benchmark',
    '100'
)
kPars = {
    'Trap': {'A': 0.5, 'b': 1},
    'Escape': {'A': 0, 'b': 100}
}

###############################################################################
# Debug check
############################################################################### 
if monet.isNotebook():
    dbg = True
    (USR, DRV) = ('dsk', 'SDR')
    randTrap = True
else:
    dbg = False
    traps = np.asarray([
        [float(argv[1]), float(argv[2])]
    ])
    TRAPS_NUM = traps.shape[0]
    randTrap = False
###############################################################################
# Read migration matrix and pop sites
############################################################################### 
pth = path.join(PT_DTA, EXP_FNAME)
migMat = np.genfromtxt(pth+'_MX.csv', delimiter=',')
sites = np.genfromtxt(pth+'_XY.csv', delimiter=',')
sitesNum = sites.shape[0]
###############################################################################
# Transitions Matrix and Base Netowrk
###############################################################################
psiN = migMat # fun.deleteLoopsFromMatrix(migMat)
# np.apply_along_axis(sum, 1, psiN)
###############################################################################
# Generate some trap locations and calculate distances
###############################################################################
(minX, minY) = np.apply_along_axis(min, 0, sites)
(maxX, maxY) = np.apply_along_axis(max, 0, sites)
if randTrap:
    traps = fun.placeTrapsRanUnif(TRAPS_NUM, (minX, maxX), (minY, maxY))
trapDists = fun.calcTrapToSitesDistance(traps, sites)
###############################################################################
# Calculate trapping probabilities and assemble matrix
###############################################################################
tProbs = fun.calcTrapsSections(trapDists, params=kPars)
tauN = fun.assembleTrapMigration(psiN, tProbs)
np.apply_along_axis(sum, 1, tauN)
# np.apply_along_axis(sum, 1, F)
###############################################################################
# Calculate metrics
###############################################################################
# Re-arrange matrix in canonical form -----------------------------------------
canO = list(range(sitesNum, sitesNum+TRAPS_NUM))+list(range(0, sitesNum))
tauCan = np.asarray([[tauN[i][j] for j in canO] for i in canO])
A = tauCan[TRAPS_NUM:, :TRAPS_NUM]
B = tauCan[TRAPS_NUM:, TRAPS_NUM:]
F = np.linalg.inv(np.subtract(np.identity(B.shape[0]), B))
daysTillTrapped = np.apply_along_axis(np.max, 1, F)
daysSum = np.mean(daysTillTrapped)
print('* Average days: {}'.format(daysSum))
###############################################################################
# Plot matrix
###############################################################################
if dbg is not True:
    (fig, ax) = plt.subplots(figsize=(15, 15))
    plt.imshow(tauN, vmax=1e-1, cmap='Purples', interpolation='nearest')
    fig.savefig(
        path.join(PT_IMG, EXP_FNAME+'_trapsMatrix.png'), 
        dpi=500, bbox_inches='tight'
    )
###############################################################################
# Plot landscape
###############################################################################
BBN = tauN[:sitesNum, :sitesNum]
BQN = tauN[:sitesNum, sitesNum:]
(LW, ALPHA, SCA) = (.125, .2, 50)
(fig, ax) = plt.subplots(figsize=(15, 15))
(fig, ax) = aux.plotNetwork(fig, ax, BQN*SCA, traps, sites, [0], c='#f72585', lw=LW*2.5, alpha=.75)
(fig, ax) = aux.plotNetwork(fig, ax, BBN*SCA, sites, sites, [0], c='#2B62F7', lw=LW, alpha=ALPHA)
plt.scatter(sites.T[0], sites.T[1], marker='^', color='#03045eDB', s=50, zorder=20)
plt.scatter(traps.T[0], traps.T[1], marker='o', color='#f72585EE', s=250, zorder=20)
# plt.tick_params(
#     axis='both', which='both',
#     bottom=False, top=False, left=False, right=False,
#     labelbottom=False, labeltop=False, labelleft=False, labelright=False
# )
ax.text(
    0.5, 1.035, 'Avg Max Days: {:.2f}'.format(daysSum),
    horizontalalignment='center',
    verticalalignment='center',
    fontsize=50, color='#000000DD',
    transform=ax.transAxes, zorder=15
)
###############################################################################
# Export figure
###############################################################################
if dbg is False:
    fig.savefig(
        path.join(
            PT_IMG, 
            '{}-{}_{}-trapsNetwork.png'.format(EXP_FNAME, int(traps[0][0]), int(traps[0][1])
            )
        ), 
        dpi=250, bbox_inches='tight'
    )
else:
    fig.savefig(
        path.join(
            PT_IMG, '{}-trapsNetwork.png'.format(EXP_FNAME)
        ), 
        dpi=250, bbox_inches='tight'
    )


