#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, AOI, REL, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# (USR, AOI, REL, LND) = ('dsk', 'ECO', 'mixed', 'PAN')
(DRV, FMT, OVW, FZ) = ('LDR', 'bz2', True, True)
###############################################################################
# Setting up paths and style
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=100*12000), 
    lnd.landSelector(LND)
)
(CLR, YRAN) = (drive.get('colors'), drive.get('yRange'))
STYLE = {
    "width": .5, "alpha": .15, "dpi": 2*300, "legend": True, "aspect": .25,
    "colors": CLR, "xRange": [0, 365 * 3], "yRange": [0, YRAN]
}
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
# Paths -----------------------------------------------------------------------
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
PT_IMG = PT_IMG + 'preTraces/'
monet.makeFolder(PT_IMG)
# Setup the run ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_ROT, PT_IMG, tS, 'UCIMI PreTraces '+AOI)
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
    monet.exportTracesPlot(repDta, name, STYLE, PT_IMG, vLines=[0, 0])
###############################################################################
# Export plot legend
###############################################################################
cl = [i[:-2]+'cc' for i in CLR]
monet.exportGeneLegend(
    sumDta['genotypes'], cl, PT_IMG+'/plt_{}.png'.format(AOI), 500
)
