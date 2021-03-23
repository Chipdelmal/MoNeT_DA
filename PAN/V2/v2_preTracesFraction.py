#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import numpy as np
import v2_aux as aux
import v2_gene as drv
# import PYF_land as lnd
import matplotlib.pyplot as plt
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0.0),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 1.0, 0.0, 0.0),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 1.0, 0.0),  # blue  with alpha = 20%
})


if monet.isNotebook():
    (USR, DRV, AOI) = ('dsk', 'SDR', 'ECO')
else:
    (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
###############################################################################
(tStable, FZ) = (50, False)
(FMT, OVW, JOB, MF) = ('bz2', False, 4, (True, True))
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
###############################################################################
# Setting up paths and drive
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR)
(expDirsMean, expDirsTrac) = monet.getExpPaths(
    PT_DTA, mean='analyzed/', reps='traces/'
)
PT_ANL = (PT_ROT + 'analyzed/E_001/')
(drive, land) = (drv.driveSelector(DRV, AOI, popSize=15000), ([0], ))
MF = (True, True)
if AOI == 'HLT':
    MF = (False, True)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_PRE, PT_IMG, tS, 'V2 PreTraces ' + AOI)
###############################################################################
# Style
###############################################################################
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": 1.25, "alpha": .15, "dpi": 1500, "legend": True,
        "aspect": .25, "colors": CLR, "xRange": [(365*1.5), (365*6)],
        "yRange": (-0, 1)
    }
if AOI == 'ECO':
    STYLE['yRange'] = (STYLE['yRange'][0], STYLE['yRange'][1]/2)
releases = [0, 0]
releases.extend(list(range(3*365, 3*365 + 7*8, 7)))
if AOI == 'HUM':
    releases = [0, 0]
###############################################################################
# Load preprocessed files lists
###############################################################################
tyTag = ('sum', 'srp')
(fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
fLists = monet.getFilteredTupledFiles(fltrPattern, globPattern, tyTag)
###############################################################################
# Process files
###############################################################################
(xpNum, digs) = monet.lenAndDigits(fLists)
for i in range(0, xpNum):
    monet.printProgress(i+1, xpNum, digs)
    (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
    name = fLists[i][0].split('/')[-1].split('.')[0][:-4]
    # Traces ------------------------------------------------------------------
    a = sumDta['population']
    balPop = [
        np.asarray([aux.zeroDivide(i, j.T[-1]) for i in j.T]).T for j in repDta['landscapes']
    ]
    fractionData = {'genotypes': repDta['genotypes'], 'landscapes': balPop}
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    # Export plots --------------------------------------------------------
    aux.exportTracesPlot(
        fractionData, name, STYLE, PT_IMG, wopPrint=False,
        vLines=releases, AOI=AOI
    )
    cl = [i[:-2]+'cc' for i in CLR]
# Export gene legend ------------------------------------------------------
monet.exportGeneLegend(
        sumDta['genotypes'], cl, PT_IMG+'/legend_{}.png'.format(AOI), 500
    )
tE = datetime.now()
###############################################################################
# Mossy Infected Plot
###############################################################################
# Mosquito Data ---------------------------------------------------------------
mossy = [i[-1] for i in pkl.load(PT_PRE + 'E_001-HLT_00_sum.bz')['population']]
infected = np.sum(
    np.loadtxt(
        PT_ANL+'FI_Mean_0001.csv', skiprows=1, delimiter=',', 
        usecols=list(range(1, 30))
    ), axis=1
)
if AOI == 'HLT':
    infct = infected / np.asarray([i[-1] for i in a])
    (fig, ax) = plt.subplots(figsize=(10, 5.5), sharex=True)
    STYLE = {
        "width": 2, "alpha": .5, "dpi": 1500, "legend": True,
        "aspect": .25, "xRange": [(365*1.5), (365*6)],
        "yRange": (0, 1)
    }
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    colors = ('#3772ffEF', )
    ax.plot(range(0, len(infct)), infct, lw=STYLE['width'], ls='-', color=colors[0])
    ax.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    ax.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    ax.set_aspect(aspect=STYLE["aspect"])
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.set_axis_off()
    fig.savefig(
            "{}/{}.png".format(PT_IMG, 'Infected'),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='png',
            transparent=True, bbox_inches='tight', pad_inches=0
        )
    plt.close('all')

