
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

TRAPS_NUM = 1
STEPS = 50
delta = 0.01
(PT_DTA, PT_IMG, EXP_FNAME) = (
    '/Volumes/marshallShare/Mov/dta',
    '/Volumes/marshallShare/Mov/trp/Benchmark',
    '00X'
)
kPars = {
    'Trap': {'A': 0.5, 'b': 1},
    'Escape': {'A': 0, 'b': 100}
}
(dbg, randTrap) = (True, True)
(USR, DRV) = ('dsk', 'SDR')
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
(minX, minY) = np.apply_along_axis(min, 0, sites)
(maxX, maxY) = np.apply_along_axis(max, 0, sites)
###############################################################################
# Generate some trap locations and calculate distances
###############################################################################
(xGrid, yGrid) = (
    np.arange(minX-delta, maxX+2*delta, (maxX-minX)/STEPS), 
    np.arange(minY-delta, maxY+2*delta, (maxY-minY)/STEPS)
) 
fits = np.zeros((len(xGrid), len(yGrid)))
(cntr, total) = (0, fits.shape[0]*fits.shape[1])
fitsDict = []
# Iterate over possible solutions ---------------------------------------------
for (r, x) in enumerate(xGrid):
    for (c, y) in enumerate(yGrid):
        traps = [[x, y]]
        trapDists = fun.calcTrapToSitesDistance(traps, sites)
        #######################################################################
        # Calculate trapping probabilities and assemble matrix
        #######################################################################
        tProbs = fun.calcTrapsSections(trapDists, params=kPars)
        tauN = fun.assembleTrapMigration(psiN, tProbs)
        np.apply_along_axis(sum, 1, tauN)
        # np.apply_along_axis(sum, 1, F)
        #######################################################################
        # Calculate metrics
        #######################################################################
        # Re-arrange matrix in canonical form ---------------------------------
        canO = list(range(sitesNum, sitesNum+TRAPS_NUM))+list(range(0, sitesNum))
        tauCan = np.asarray([[tauN[i][j] for j in canO] for i in canO])
        A = tauCan[TRAPS_NUM:, :TRAPS_NUM]
        B = tauCan[TRAPS_NUM:, TRAPS_NUM:]
        F = np.linalg.inv(np.subtract(np.identity(B.shape[0]), B))
        daysTillTrapped = np.apply_along_axis(np.max, 1, F)
        daysSum = np.mean(daysTillTrapped)
        # Arrange fits --------------------------------------------------------
        cntr = cntr + 1
        fits[r, c] = daysSum
        fitsDict.append([x, y, daysSum])
        #######################################################################
        # Print message
        #######################################################################
        print(
            '* Processed {}/{}: {:.2f}'.format(cntr, total, daysSum), 
            end='\r'
        )
# plt.imshow(fits, vmin=0, vmax=20, cmap='Purples', interpolation='nearest')
###############################################################################
# Get best location
###############################################################################
fitsVals = [i[2] for i in fitsDict]
(best, worst) = (min(fitsVals), max(fitsVals))
ix = fitsVals.index(best)
traps = np.asarray([[fitsDict[ix][0], fitsDict[ix][1]]])
trapDists = fun.calcTrapToSitesDistance(traps, sites)
#######################################################################
# Calculate trapping probabilities and assemble matrix
#######################################################################
tProbs = fun.calcTrapsSections(trapDists, params=kPars)
tauN = fun.assembleTrapMigration(psiN, tProbs)
###############################################################################
# Plot landscape
###############################################################################
rvb = monet.colorPaletteFromHexList(['#ffffff',  '#9b5de5', '#00296b'])
BBN = tauN[:sitesNum, :sitesNum]
BQN = tauN[:sitesNum, sitesNum:]
(LW, ALPHA, SCA) = (.125, .5, 50)
(fig, ax) = plt.subplots(figsize=(15, 15))
(fig, ax) = aux.plotNetwork(fig, ax, BQN*SCA, traps, sites, [0], c='#f72585', lw=LW*3, alpha=.9)
(fig, ax) = aux.plotNetwork(fig, ax, BBN*SCA, sites, sites, [0], c='#03045e', lw=LW, alpha=ALPHA)
plt.scatter(
    sites.T[0], sites.T[1], 
    marker='^', color='#03045eDB', 
    s=250, zorder=20, edgecolors='w', linewidths=2
)
plt.scatter(
    traps.T[0], traps.T[1], 
    marker='X', color='#f72585EE', s=500, zorder=20,
    edgecolors='w', linewidths=2
)
for point in fitsDict:
    plt.scatter(
        point[0], point[1], 
        marker='s', color=rvb((point[2]-best)/(.25*(worst-best))), 
        alpha=.5,
        s=250, zorder=-5,
        linewidths=0, edgecolors='k'
    )
plt.tick_params(
    axis='both', which='both',
    bottom=False, top=False, left=False, right=False,
    labelbottom=False, labeltop=False, labelleft=False, labelright=False
)
ax.text(
    0.5, 1.035, 'Avg Max Days: {:.2f}'.format(best),
    horizontalalignment='center',
    verticalalignment='center',
    fontsize=50, color='#000000DD',
    transform=ax.transAxes, zorder=15
)
ax.set_aspect('equal')
ax.set_xlim(minX-.1, maxX+.1)
ax.set_ylim(minY-.1, maxY+.1)
###############################################################################
# Export figure
###############################################################################
fig.savefig(
    path.join(PT_IMG, '{}-BF-trapsNetwork.png'.format(EXP_FNAME)), 
    dpi=250, bbox_inches='tight'
)
plt.close()

