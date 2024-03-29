
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
from scipy.interpolate import interp1d

if monet.isNotebook():
    (EXP_FNAME, TRAPS_NUM) = ('UNIF_MD-200-HET', 1)
    (PT_DTA, PT_IMG) = aux.selectPaths('lab')
else:
    (EXP_FNAME, TRAPS_NUM) = (argv[1], 1)
    (PT_DTA, PT_IMG) = aux.selectPaths(argv[2])
kPars = aux.KPARS
(LAY_TRAP, STEPS, delta) = (False, 120, 0.01)
###############################################################################
# Read migration matrix and pop sites 
############################################################################### 
pth = path.join(PT_DTA, EXP_FNAME)
migMat = np.genfromtxt(pth+'_MX.csv', delimiter=',')
sites = np.genfromtxt(pth+'_XY.csv', delimiter=',')
sitesNum = sites.shape[0]
pTypes = None
if sites.shape[1] > 2:
    pTypes = sites[:,2]
    sites = sites[:, 0:2]
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
        #######################################################################
        # Calculate metrics
        #######################################################################
        # Re-arrange matrix in canonical form ---------------------------------
        tauCan = fun.reshapeInCanonicalForm(tauN, sitesNum, TRAPS_NUM)
        F = fun.getMarkovAbsorbing(tauCan, TRAPS_NUM)
        daysTillTrapped = np.apply_along_axis(np.mean, 1, F)
        daysSum = np.mean(daysTillTrapped)
        # Arrange fits --------------------------------------------------------
        cntr = cntr + 1
        fits[r, c] = daysSum
        fitsDict.append([x, y, daysSum])
        #######################################################################
        # Print message
        #######################################################################
        print(
            '* Processed {}/{}: {:.2f}'.format(cntr, total, daysSum), end='\r'
        )
###############################################################################
# Get best location
###############################################################################
fitsVals = [i[2] for i in fitsDict]
(best, mean, worst) = (min(fitsVals), np.mean(fitsVals), max(fitsVals))
ix = fitsVals.index(best)
traps = np.asarray([[fitsDict[ix][0], fitsDict[ix][1]]])
trapDists = fun.calcTrapToSitesDistance(traps, sites)
###############################################################################
# Calculate trapping probabilities and assemble matrix
###############################################################################
tProbs = fun.calcTrapsSections(trapDists, params=kPars)
tauN = fun.assembleTrapMigration(psiN, tProbs)
###############################################################################
# Plot landscape
###############################################################################
inteRange = (best, mean)
m = interp1d(inteRange, [2.5, -2.5])
(BBN, BQN) = (tauN[:sitesNum, :sitesNum], tauN[:sitesNum, sitesNum:])
(LW, ALPHA, SCA) = (.125, .5, 50)
# Generate figure -------------------------------------------------------------
(fig, ax) = plt.subplots(figsize=(15, 15))
# Plot networks ---------------------------------------------------------------
(fig, ax) = aux.plotNetwork(
    fig, ax, BBN*SCA, sites, sites, [0], c='#03045e', lw=LW, alpha=ALPHA
)
if LAY_TRAP:
    (fig, ax) = aux.plotNetwork(
        fig, ax, BQN*SCA, traps, sites, [0], c='#f72585', lw=LW*3, alpha=.9
    )
# Plot sites and traps --------------------------------------------------------
if pTypes is None:
    plt.scatter(
        sites.T[0], sites.T[1], 
        marker='^', color='#03045eDB', 
        s=250, zorder=20, edgecolors='w', linewidths=2
    )
else:
    for (i, site) in enumerate(sites):
        plt.scatter(
            site[0], site[1], 
            marker=aux.MKRS[int(pTypes[i])], color=aux.MCOL[int(pTypes[i])], 
            s=200, zorder=20, edgecolors='w', linewidths=2
        )    
if LAY_TRAP:
    plt.scatter(
        traps.T[0], traps.T[1], 
        marker='+', color='#f72585EE', 
        s=250, zorder=20, edgecolors='w', linewidths=2
    )
# Plot response surface -------------------------------------------------------
for point in fitsDict[:]:
    smp = min(point[2], inteRange[1])
    csca = 1/(1+math.exp(m(smp)))
    plt.scatter(
        point[0], point[1], 
        marker='.', color=aux.RVB(csca), 
        alpha=.2, s=25, zorder=-5, linewidths=0, edgecolors='#12121200'
    )
# Axes and title --------------------------------------------------------------
plt.tick_params(
    axis='both', which='both',
    bottom=False, top=False, left=False, right=False,
    labelbottom=False, labeltop=False, labelleft=False, labelright=False
)
ax.set_aspect('equal')
ax.set_xlim(minX, maxX)
ax.set_ylim(minY, maxY)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
# Export figure ---------------------------------------------------------------
fig.savefig(
    path.join(PT_IMG, '{}-BF-NET.png'.format(EXP_FNAME)), 
    dpi=250, bbox_inches='tight', pad_inches=0
)
plt.close()

