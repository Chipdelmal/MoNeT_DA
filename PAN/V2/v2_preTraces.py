#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import v2_aux as aux
import v2_gene as drv
# import PYF_land as lnd
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


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
(drive, land) = (drv.driveSelector(DRV, AOI, popSize=15000), ([0], ))
MF = (True, True)
if AOI == 'HLT':
    MF = (False, True)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_ROT, PT_PRE, tS, 'V2 Preprocess '+AOI)
###############################################################################
# Style
###############################################################################
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": .1, "alpha": .1, "dpi": 1500, "legend": True,
        "aspect": .25, "colors": CLR, "xRange": [0, (365*10)],
        "yRange": YRAN
    }
tS = datetime.now()
monet.printExperimentHead(PT_PRE, PT_IMG, tS, 'V2 PreTraces ' + AOI)
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
    balPop = max([max(i) for i in sumDta['population']])
    STYLE['yRange'] = (0,  balPop/2+balPop*.5)
    if AOI == 'ECO':
        STYLE['yRange'] = (STYLE['yRange'][0], balPop * 1.1)
    STYLE['aspect'] = monet.scaleAspect(.125, STYLE)
    # Export plots --------------------------------------------------------
    monet.exportTracesPlot(repDta, name, STYLE, PT_IMG, wopPrint=False)
    cl = [i[:-2]+'cc' for i in CLR]
# Export gene legend ------------------------------------------------------
print(sumDta)
monet.exportGeneLegend(
        sumDta['genotypes'], cl, PT_IMG+'/legend_{}.png'.format(AOI), 500
    )
tE = datetime.now()
