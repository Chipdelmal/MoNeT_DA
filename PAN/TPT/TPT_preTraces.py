#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
from more_itertools import locate
from os import path
import compress_pickle as pkl
import TPT_aux as aux
import TPT_gene as drv
import TPT_functions as fun


if monet.isNotebook():
    (USR, AOI, DRV, SPE) = ('srv', 'INC', 'LDR', 'gambiae_low')
else:
    (USR, AOI, DRV, SPE) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
EXPS = aux.getExps()
exp = EXPS[0]
for exp in EXPS:
    ###########################################################################
    # Setting up paths
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE, humSize=aux.HUM_SIZE),
        aux.landSelector(USR=USR)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, DRV, SPE
    )
    # Time and head -----------------------------------------------------------
    PT_IMG = path.join(PT_IMG, 'preTraces')
    monet.makeFolder(PT_IMG)
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .75, "alpha": .5, "dpi": 500, "legend": True,
            "aspect": 1/6, "colors": CLR, 
            "xRange": aux.XRAN, "yRange": [0, YRAN[1]]
        }
    tS = datetime.now()
    monet.printExperimentHead(
        PT_PRE, PT_IMG, tS, 
        '{} PreTraces [{}:{}:{}]'.format(aux.XP_ID, fldr, exp, AOI)
    )
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    tyTag = ('sum', 'srp')
    (fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
    if aux.FZ:
        fltrPattern = PT_PRE + aux.patternForReleases('00', AOI, '*')
    fLists = monet.getFilteredTupledFiles(fltrPattern, globPattern, tyTag)
    expNum = len(fLists)
    # Arrange file tuples -----------------------------------------------------
    expIter = list(zip(list(range(expNum, 0, -1)), fLists))
    expIter.reverse()
    # NEEDS OVW FITLERING!!!!!!!!!! -------------------------------------------
    ###########################################################################
    # Process files
    ###########################################################################
    (xpNum, digs) = monet.lenAndDigits(fLists)
    Parallel(n_jobs=JOB)(
        delayed(fun.exportPreTracesParallel)(
            exIx, STYLE, PT_IMG, 
            xpNum=xpNum, digs=digs, autoAspect=True,
            border=True, borderColor='#000000AA', borderWidth=1,
            sampRate=1, vLines=aux.RELEASES
        ) for exIx in expIter
    )
    # Export gene legend ------------------------------------------------------
    # sumDta = pkl.load(fLists[-1][0])
    # monet.exportGeneLegend(
    #     sumDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
    #     PT_IMG+'/legend_{}.png'.format(AOI), 500
    # )

