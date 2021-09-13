#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
from datetime import datetime
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import compress_pickle as pkl


if monet.isNotebook():
    (USR, AOI, LND, DRV) = ('dsk', 'HLT', 'PAN', 'LDR')
    JOB = aux.JOB_DSK
else:
    (USR, AOI, LND, DRV) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
EXPS = aux.getExps(LND)
exp = EXPS[0]
for exp in EXPS:
    ###########################################################################
    # Setting up paths
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
        lnd.landSelector(exp, LND, USR=USR)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, LND, DRV
    )
    PT_IMG = path.join(PT_IMG, 'preTraces')
    monet.makeFolder(PT_IMG)
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .75, "alpha": .75, "dpi": 500, "legend": True,
            "aspect": 1, "colors": CLR, "xRange": aux.XRAN, "yRange": [0, YRAN[1]/7.5]
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
        delayed(dbg.exportPreTracesParallel)(
            exIx, STYLE, PT_IMG, 
            xpNum=xpNum, digs=digs, autoAspect=True,
            border=True, borderColor='#8184a7AA', borderWidth=2
        ) for exIx in expIter
    )
    # Export gene legend ------------------------------------------------------
    # sumDta = pkl.load(fLists[-1][0])
    # monet.exportGeneLegend(
    #     sumDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
    #     PT_IMG+'/legend_{}.png'.format(AOI), 500
    # )
