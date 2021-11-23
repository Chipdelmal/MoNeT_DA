
import time
import math
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
import TRP_fun as fun
import MoNeT_MGDrivE as monet
from deap import base, creator, algorithms, tools
from PIL import Image
import subprocess


if monet.isNotebook():
    (EXP_FNAME, TRAPS_NUM) = ('DNT_03-100-HET', 4)
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths('lab')
else:
    (EXP_FNAME, TRAPS_NUM) = (argv[1], int(argv[2]))
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths(argv[3])
fName = '{}_{}_GA'.format(EXP_FNAME, TRAPS_NUM)
(LW, ALPHA, SCA) = (.125, .5, 50)
pklPath = path.join(
    PT_GA, '{}_{}_GA'.format(EXP_FNAME, str(TRAPS_NUM).zfill(2))
)
(LW, ALPHA, SCA) = (.125, .5, 15)
###############################################################################
# Read bg image
###############################################################################
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
# Read GA data ----------------------------------------------------------------
with open(pklPath+'.pkl', "rb") as file:
    gaRAW = pkl.load(file)
###############################################################################
# Plot landscape
###############################################################################
outPTH = path.join(PT_IMG, fName)
monet.makeFolder(outPTH)
i = 1
framesNum = gaRAW.shape[0]
for i in range(50, 100):
    print('* Processed: {}/{}'.format(i, framesNum), end='\r')
    background = Image.open(path.join(PT_IMG, bgImg))
    # Subset GA data ----------------------------------------------------------
    ga = gaRAW[:i]
    cols = [ga['max'], ga['mean'], ga['min'], ga['traps']]
    (maxFits, meanFits, minFits, traps) = [list(i) for i in cols]
    (bestVal, bestIx) = min((val, idx) for (idx, val) in enumerate(minFits))
    best = ga['traps'].iloc[bestIx]
    meanGA = list(ga['mean'])[-1]
    # Assemble migration with traps -------------------------------------------
    trapsLocs = list(np.array_split(best, len(best)/2))
    trapDists = fun.calcTrapToSitesDistance(trapsLocs, sites)
    tProbs = fun.calcTrapsSections(trapDists, params=aux.KPARS)
    tauN = fun.assembleTrapMigration(migMat, tProbs)
    BBN = tauN[:sitesNum, :sitesNum]
    BQN = tauN[:sitesNum, sitesNum:]
    (tpPrs, tRan) = (aux.KPARS['Trap'], [.25, .1, .05, .01])
    radii = [math.log(tpPrs['A']/y)/(tpPrs['b']) for y in tRan]
    # Plot --------------------------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(15, 15))
    (fig, ax) = aux.plotTraps(
        fig, ax, trapsLocs, bestVal, sites, pTypes, radii, BQN,
        minX, minY, maxX, maxY, gen=meanGA, sca=SCA, lw=LW, alpha=ALPHA
    )
    # Export ------------------------------------------------------------------
    pthSave = path.join(outPTH, str(i).zfill(4)+'.png')
    fig.savefig(
        pthSave, dpi=aux.DPI, bbox_inches='tight', 
        pad_inches=0, transparent=True
    )
    plt.close('all')
    # Merge -------------------------------------------------------------------
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
###############################################################################
# Export video
###############################################################################
sp = subprocess.Popen([
    'ffmpeg', '-y',
    '-start_number', '1',
    '-r', '4',
    '-i', path.join(outPTH, "%04d.png"), 
    # '-vf', 'scale=1000:1000',
    path.join(outPTH, fName+'.mp4')
])
sp.wait()

