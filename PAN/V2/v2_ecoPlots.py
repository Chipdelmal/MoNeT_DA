

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import v2_aux as aux
import v2_gene as drv
import pandas as pd
import numpy as np
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt


if monet.isNotebook():
    (USR, DRV, AOI) = ('dsk', 'SDR', 'HLT')
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
PT_GEO = (PT_ROT + 'GEO/')
PT_TRA = (PT_ROT + 'epitraces/E_001/')
(drive, land) = (drv.driveSelector(DRV, AOI, popSize=15000), ([0], ))
MF = (True, True)
if AOI == 'HLT':
    MF = (False, True)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_ROT, PT_PRE, tS, 'V2 Preprocess '+AOI)
###############################################################################
# Reading data
###############################################################################
rainfall = np.loadtxt(
    PT_GEO+'Rainfall/km_precip_2010s_daily.csv',
    skiprows=1, delimiter=',', usecols=(0, )
)
temperature = np.loadtxt(
    PT_GEO+'Temperature/km_temp_2010s.csv',
    skiprows=1, delimiter=',', usecols=(0, )
)
# Epi Data --------------------------------------------------------------------
stpPop = 350998
epiFiles = sorted(glob(PT_TRA+'/incidence*.csv'))
epi = [np.loadtxt(i, skiprows=1, delimiter=',', usecols=(1, )) for i in epiFiles]
epi = [[i / stpPop * 1000 for i in j] for j in epi]
epiMx = max([max(i) for i in epi])
###############################################################################
# Epi Plots
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 5.5), sharex=True)
STYLE = {
    "width": .0075, "alpha": .5, "dpi": 1500, "legend": True,
    "aspect": .25, "xRange": [0, (365*10)],
    "yRange": (0, 1)
}
STYLE['aspect'] = monet.scaleAspect(.125, STYLE)
colors = ('#f200600C', '#f2006059')
for i in epi:
    tmp = [j/epiMx for j in i]
    ax.plot(range(0, len(tmp)), tmp, lw=STYLE['width'], color=colors[1])
for vline in list(range(3*365, 3*365 + 7*8, 7)):
    ax.axvline(vline, alpha=.75, zorder=10, lw=.1, color='#000000')
ax.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
ax.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
ax.set_aspect(aspect=STYLE["aspect"])
ax.axes.xaxis.set_ticklabels([])
ax.axes.yaxis.set_ticklabels([])
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax.set_axis_off()
fig.savefig(
        "{}/{}.png".format(PT_IMG, 'EPI'),
        dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
        orientation='portrait', papertype=None, format='png',
        transparent=True, bbox_inches='tight', pad_inches=0
    )
plt.close('all')