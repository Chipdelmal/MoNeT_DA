
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
from PIL import Image


(PT_DTA, PT_IMG, EXP_FNAME, TRAPS_NUM) = (
    '/Volumes/marshallShare/Mov/dta',
    '/Volumes/marshallShare/Mov/trp',
    '300', '25'
)
fName = '{}_{}-GA'.format(EXP_FNAME, TRAPS_NUM)
(LW, ALPHA, SCA) = (.125, .5, 50)
###############################################################################
# Read bg image
###############################################################################
bgImg = '{}-BF-trapsNetwork.png'.format(EXP_FNAME)
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
sitesNum = sites.shape[0]
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
i = 0
for i in range(len(trapsHistory)):
    background = Image.open(path.join(PT_IMG, bgImg))
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
        0.5, 0.5, '{:.4f}'.format(minHistory[i]),
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=150, color='#00000022',
        transform=ax.transAxes, zorder=50
    )
    ax.text(
        0.925, 0.025, '{}'.format(str(i).zfill(4)),
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=25, color='#ffffff77',
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
    pthSave = path.join(outPTH, str(i).zfill(3)+'.png')
    fig.savefig(
        pthSave, dpi=250, bbox_inches='tight', transparent=True
    )
    plt.close()
    # Merge -------------------------------------------------------------------
    foreground = Image.open(pthSave)
    # (w, h) = foreground.size
    # background = background.crop((0, 0, w, h))
    background.paste(foreground, (0, 0), foreground)
    background.save(pthSave)

