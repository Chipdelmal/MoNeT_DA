#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import PYF_aux as aux
import PYF_gene as drv
import PYF_land as lnd
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl

if monet.isNotebook():
    (USR, DRV, AOI, LND) = ('dsk', 'PGS', 'HLT', 'PAN')
else:
    (USR, DRV, AOI, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
(FZ, tStable) = (False, int(30/2))
###############################################################################
# Setting up paths
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND)
PT_IMG = PT_IMG + 'preTraces/'
monet.makeFolder(PT_IMG)
###############################################################################
# Load landscape and drive
###############################################################################
drive = drv.driveSelector(DRV, AOI, popSize=20*62)
land = lnd.landSelector(LND, PT_ROT)
gene = drive.get('gDict')
###############################################################################
# Style 
###############################################################################
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": .3, "alpha": .5, "dpi": 300, "legend": True,
        "aspect": .25, "colors": CLR, "xRange": [0, (365*2.5)],
        "yRange": YRAN
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
tS = datetime.now()
monet.printExperimentHead(PT_PRE, PT_IMG, tS, 'PreTraces ' + AOI)
###############################################################################
# Load preprocessed files lists
###############################################################################
tyTag = ('sum', 'srp')
(fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
if FZ:
    fltrPattern = PT_PRE+'*_00_*'+AOI+'*'+'{}'+'*'
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
    balPop = sum(sumDta['population'][tStable])
    STYLE['yRange'] = (0,  balPop/2+balPop*.5)
    if AOI == 'ECO':
        STYLE['yRange'] = (STYLE['yRange'][0], STYLE['yRange'][1]*2)
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    # Export plots --------------------------------------------------------
    monet.exportTracesPlot(repDta, name, STYLE, PT_IMG, wopPrint=False)
    cl = [i[:-2]+'cc' for i in CLR]
# Export gene legend ------------------------------------------------------
monet.exportGeneLegend(
        sumDta['genotypes'], cl, PT_IMG+'/legend_{}.png'.format(AOI), 500
    )
tE = datetime.now()
