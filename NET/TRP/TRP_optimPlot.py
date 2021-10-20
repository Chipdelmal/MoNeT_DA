
from glob import glob
import numpy as np
from os import path
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from deap import base, creator, algorithms, tools
import pickle as pkl
import TRP_gaFun as ga
import MoNeT_MGDrivE as monet
from deap import base, creator, algorithms, tools


(PT_DTA, PT_IMG, EXP_FNAME, TRAPS_NUM) = (
    '/home/chipdelmal/Documents/WorkSims/Mov/dta',
    '/home/chipdelmal/Documents/WorkSims/Mov/trp/',
    '100', '02'
)
fName = '{}_{}-GA'.format(EXP_FNAME, TRAPS_NUM)
(LW, ALPHA, SCA) = (.125, .5, 50)
###############################################################################
# Load GA data
###############################################################################
with open(path.join(PT_IMG, fName+'.pkl'), 'rb') as f:
    dta = pkl.load(f)
###############################################################################
# Read migration matrix and pop sites
############################################################################### 
pthBase = path.join(PT_DTA, EXP_FNAME)
migMat = np.genfromtxt(pthBase+'_MX.csv', delimiter=',')
sites = np.genfromtxt(pthBase+'_XY.csv', delimiter=',')
BBN = migMat[:sitesNum, :sitesNum]
BQN = migMat[:sitesNum, sitesNum:]
# Sites and landscape shapes --------------------------------------------------
sitesNum = sites.shape[0]
(minX, minY) = np.apply_along_axis(min, 0, sites)
(maxX, maxY) = np.apply_along_axis(max, 0, sites)
(xMinMax, yMinMax) = ((minX, maxX), (minY, maxY))
# Get traps -------------------------------------------------------------------
trapsHistory = dta['traps']
minHistory = dta['min']
###############################################################################
# Plot landscape
###############################################################################
outPTH = path.join(PT_IMG, fName)
monet.makeFolder(outPTH)

for i in range(len(trapsHistory)):
    trapsLocs = trapsLocs = list(
        np.array_split(trapsHistory[i], len(trapsHistory[i])/2)
    )
    # Plot --------------------------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(15, 15))
    plt.scatter(
        sites.T[0], sites.T[1], 
        marker='^', color='#03045eDB', 
        s=250, zorder=20, edgecolors='w', linewidths=2
    )
    for trap in trapsLocs:
        plt.scatter(
            trap[0], trap[1], 
            marker="X", color='#f72585EE', s=500, zorder=20,
            edgecolors='w', linewidths=2
        )
    ax.text(
        0.5, 0.5, '{:.2f}'.format(minHistory[i]),
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=200, color='#00000033',
        transform=ax.transAxes, zorder=50
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
    # Export ------------------------------------------------------------------
    fig.savefig(
        path.join(
            outPTH, str(i).zfill(3)
        ), 
        dpi=250, bbox_inches='tight', transparent=True
    )
    plt.close()