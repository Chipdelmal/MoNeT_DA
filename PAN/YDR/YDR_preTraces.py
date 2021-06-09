#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob

from numpy.core.fromnumeric import transpose
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd
from datetime import datetime
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt

plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0.0),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 1.0, 0.0, 0.0),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 1.0, 0.0),  # blue  with alpha = 20%
})

if monet.isNotebook():
    (USR, SET, DRV, AOI) = ('dsk', 'shredder', 'YXS', 'WLD')
    JOB = aux.JOB_DSK
else:
    (USR, SET, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    JOB = aux.JOB_SRV

###############################################################################
# Setting up paths and style
###############################################################################
EXPS = aux.EXPS
exp=EXPS[0]
for exp in EXPS:
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
        lnd.landSelector('SPA')
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, exp
    )
    PT_IMG = PT_IMG + 'preTraces/'
    monet.makeFolder(PT_IMG)
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .075, "alpha": .1, "dpi": 1000, "legend": True,
            "aspect": .25, "colors": CLR, "xRange": aux.XRAN, "yRange": YRAN
        }
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    tS = datetime.now()
    monet.printExperimentHead(
        PT_PRE, PT_IMG, tS, 
        aux.XP_ID+' PreTraces [{}:{}:{}]'.format(DRV, exp, AOI)
    )
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    tyTag = ('sum', 'srp')
    (fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
    if aux.FZ:
        fltrPattern = PT_PRE + aux.patternForReleases('homing', '00', AOI, '*')
    fLists = monet.getFilteredTupledFiles(fltrPattern, globPattern, tyTag)
    ###########################################################################
    # Process files
    ###########################################################################
    (xpNum, digs) = monet.lenAndDigits(fLists)
    Parallel(n_jobs=JOB)(
        delayed(monet.exportPreTracesPlotWrapper)(
            exIx, fLists, STYLE, PT_IMG, 
            xpNum=xpNum, digs=digs, 
            border=True, borderColor='#8184a7AA', borderWidth=2,
            transparent=True
        ) for exIx in range(0, len(fLists))
    )
    # Export gene legend ------------------------------------------------------
    sumDta = pkl.load(fLists[-1][0])
    monet.exportGeneLegend(
        sumDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
        PT_IMG+'/legend_{}.png'.format(AOI), 500
    )


