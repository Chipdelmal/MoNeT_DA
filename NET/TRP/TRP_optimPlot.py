
import time
from sys import argv
from glob import glob
import numpy as np
from os import path
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from deap import base, creator, algorithms, tools
import pickle as pkl
import TRP_gaFun as ga
import TRP_aux as aux
import MoNeT_MGDrivE as monet
from deap import base, creator, algorithms, tools
from PIL import Image
import subprocess


if monet.isNotebook():
    (EXP_FNAME, TRAPS_NUM) = ('001', 20)
    (PT_DTA, PT_IMG) = aux.selectPaths('dsk')
else:
    (EXP_FNAME, TRAPS_NUM) = (argv[1], int(argv[2]))
    (PT_DTA, PT_IMG) = aux.selectPaths(argv[3])
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
meanHistory = dta['mean']
minHistory = dta['min']
###############################################################################
# Plot landscape
###############################################################################
outPTH = path.join(PT_IMG, fName)
monet.makeFolder(outPTH)
i = 0
framesNum = len(trapsHistory)
for i in list(reversed(list(range(framesNum)))):
    print('* Processed: {}/{}'.format(i, framesNum), end='\r')
    background = Image.open(path.join(PT_IMG, bgImg))
    trapsLocs = trapsLocs = list(
        np.array_split(trapsHistory[i], len(trapsHistory[i])/2)
    )
    # Plot --------------------------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(15, 15))
    # plt.scatter(
    #     sites.T[0], sites.T[1], 
    #     marker='^', color='#03045eDB', 
    #     s=250, zorder=20, edgecolors='w', linewidths=2
    # )
    for trap in trapsLocs:
        plt.scatter(
            trap[0], trap[1], 
            marker="X", color='#f72585EE', s=500, zorder=20,
            edgecolors='w', linewidths=2
        )
    ax.text(
        0.5, 0.5, '{:.3f}'.format(minHistory[i]),
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=150, color='#00000022',
        transform=ax.transAxes, zorder=50
    )
    ax.text(
        0.5, 0.4, '(avg: {:.5f})'.format(meanHistory[i]),
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=30, color='#00000022',
        transform=ax.transAxes, zorder=50
    )
    # ax.text(
    #     0.925, 0.025, '{}'.format(str(i).zfill(4)),
    #     horizontalalignment='center',
    #     verticalalignment='center',
    #     fontsize=25, color='#ffffff77',
    #     transform=ax.transAxes, zorder=50
    # )
    plt.tick_params(
        axis='both', which='both',
        bottom=False, top=False, left=False, right=False,
        labelbottom=False, labeltop=False, labelleft=False, labelright=False
    )
    ax.patch.set_facecolor('white')
    ax.patch.set_alpha(0)
    ax.set_aspect('equal')
    ax.set_xlim(minX, maxX)
    ax.set_ylim(minY, maxY)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # Export ------------------------------------------------------------------
    pthSave = path.join(outPTH, str(i).zfill(4)+'.png')
    fig.savefig(
        pthSave, dpi=250, bbox_inches='tight', transparent=True
    )
    # Merge -------------------------------------------------------------------
    time.sleep(3)
    foreground = Image.open(pthSave)
    (w, h) = background.size
    background = background.crop((0, 0, w, h))
    foreground = foreground.resize((int(w/1), int(h/1)),Image.ANTIALIAS)
    background.paste(foreground, (0, 0), foreground)
    # background = foreground.resize((int(w/1), int(h/1)),Image.ANTIALIAS)
    background.save(pthSave)
    background.close()
    foreground.close()
    plt.close('all')
###############################################################################
# Export video
###############################################################################
sp = subprocess.Popen([
    'ffmpeg', '-y',
    '-start_number', '0',
    '-r', '10',
    '-i', path.join(outPTH, "%04d.png"), 
    # '-vf', 'scale=1000:1000',
    path.join(outPTH, fName+'.mp4')
])
sp.wait()
