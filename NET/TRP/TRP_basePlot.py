
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
    (EXP_FNAME, TRAPS_NUM) = ('LRG_01-350-HOM', 1)
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths('lab')
else:
    (EXP_FNAME, TRAPS_NUM) = (argv[1], 1)
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths(argv[2])
kPars = aux.KPARS
(LAY_TRAP, STEPS) = (False, 120)
print('* Generating base plot: {}'.format(EXP_FNAME))
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
# Plot landscape
###############################################################################
(BBN, BQN) = (psiN[:sitesNum, :sitesNum], psiN[:sitesNum, sitesNum:])
(LW, ALPHA, SCA) = (.125, .5, 50)
# Generate figure -------------------------------------------------------------
(fig, ax) = plt.subplots(figsize=(15, 15))
# Plot networks ---------------------------------------------------------------
(fig, ax) = aux.plotNetwork(
    fig, ax, 
    BBN*SCA, 
    sites, sites, [0], c='#03045e', lw=LW, alpha=ALPHA
)
# Plot sites and traps --------------------------------------------------------
if pTypes is None:
    plt.scatter(
        sites.T[0], sites.T[1], 
        marker='^', color='#03045eDB', 
        s=150, zorder=20, edgecolors='w', linewidths=1.5
    )
else:
    for (i, site) in enumerate(sites):
        plt.scatter(
            site[0], site[1], 
            marker=aux.MKRS[int(pTypes[i])], color=aux.MCOL[int(pTypes[i])], 
            s=150, zorder=20, edgecolors='w', linewidths=1.5
        )    
# Axes and title --------------------------------------------------------------
plt.tick_params(
    axis='both', which='both',
    bottom=False, top=False, left=False, right=False,
    labelbottom=False, labeltop=False, labelleft=False, labelright=False
)
ax.set_aspect('equal')
ax.set_xlim(minX-aux.PAD, maxX+aux.PAD)
ax.set_ylim(minY-aux.PAD, maxY+aux.PAD)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
# Export figure ---------------------------------------------------------------
fig.savefig(
    path.join(PT_IMG, '{}_BF.png'.format(EXP_FNAME)), 
    dpi=aux.DPI, bbox_inches='tight', pad_inches=0
)
plt.close()

