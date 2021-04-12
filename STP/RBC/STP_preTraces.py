#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
from datetime import datetime
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import compress_pickle as pkl


if monet.isNotebook():
    (USR, AOI, EXP, LND) = ('dsk', 'ECO', 'PAN', 'PAN')
    JOB = aux.JOB_DSK
else:
    (USR, AOI, EXP, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    JOB = aux.JOB_SRV
###########################################################################
# Setting up paths
###########################################################################
(drive, land) = (
    drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXP, LND)
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, EXP, LND
)
PT_IMG = path.join(PT_IMG, 'preTraces')
monet.makeFolder(PT_IMG)
###########################################################################
# Style 
###########################################################################
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": .2, "alpha": .5, "dpi": 300, "legend": True,
        "aspect": 1, "colors": CLR, "xRange": aux.XRAN, "yRange": YRAN
    }
tS = datetime.now()
monet.printExperimentHead(
    PT_PRE, PT_IMG, tS, 
    '{} PreTraces [{}:{}:{}]'.format(aux.XP_ID, aux.DRV, EXP, AOI)
)
###########################################################################
# Load preprocessed files lists
###########################################################################
tyTag = ('sum', 'srp')
(fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
if aux.FZ:
    fltrPattern = PT_PRE + aux.patternForReleases('00', AOI, '*')
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
        autoAspect=True, popScaler=5
    ) for exIx in range(0, len(fLists))
)
# Export gene legend ------------------------------------------------------
sumDta = pkl.load(fLists[-1][0])
monet.exportGeneLegend(
    sumDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
    PT_IMG+'/legend_{}.png'.format(AOI), 500
)