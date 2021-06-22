#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from glob import glob
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd


if monet.isNotebook():
    (USR, SET, DRV, AOI, QNT, THS) = (
        'dsk', 'homing', 'ASD', 'HLT', '50', '0.5'
    )
    JOB = aux.JOB_DSK
else:
    (USR, SET, DRV, AOI, QNT, THS) = (
        sys.argv[1], sys.argv[2], sys.argv[3], 
        sys.argv[4], sys.argv[5], sys.argv[6]
    )
    JOB = aux.JOB_SRV
###############################################################################
(header, xpidIx) = list(zip(*aux.getSummaryHeader(SET)))
xpPat = aux.getXPPattern(SET)
###############################################################################
EXPS = aux.EXPS
exp = EXPS[0]
for exp in EXPS:
    ###########################################################################
    # Load landscape and drive
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE), 
        lnd.landSelector('SPA')
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    xpPat = aux.getXPPattern(SET)
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, exp
    )
    PT_IMG = PT_IMG + 'pstTraces/'
    monet.makeFolder(PT_IMG)
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_OUT, PT_IMG, tS, 
        aux.XP_ID+' PstProcess [{}:{}:{}]'.format(DRV, exp, AOI)
    )
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .075, "alpha": .1, "dpi": 1000, "legend": True,
            "aspect": .25, "colors": CLR, "xRange": aux.XRAN, "yRange": YRAN
        }
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    ###########################################################################
    # Load postprocessed files
    ###########################################################################
    ###########################################################################
    pstPat = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
    pstFiles = [pstPat.format(i) for i in aux.DATA_NAMES]
    (dfTTI, dfTTO, dfWOP, dfRAP, dfMNX, dfPOE, dfCPT, dfDER) = [
        pd.read_csv(i) for i in pstFiles
    ]
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    (fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
    if aux.FZ:
        fltrPattern = aux.patternForReleases(SET, '00', AOI, 'srp', ext='bz')
    repFiles = monet.getFilteredFiles(
        PT_PRE+fltrPattern, globPattern.format('srp')
    )
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    (fNum, digs) = monet.lenAndDigits(repFiles)
    Parallel(n_jobs=JOB)(
        delayed(monet.exportPstTracesPlotWrapper)(
        exIx, repFiles, xpidIx,
        dfTTI, dfTTO, dfWOP, dfMNX, dfPOE, dfCPT,
        aux.STABLE_T, THS, QNT, STYLE, PT_IMG,
        digs=digs, popScaler=1, border=True, 
        ) for exIx in range(0, len(repFiles))
    )
    # Export gene legend ------------------------------------------------------
    repDta = pkl.load(repFiles[-1])
    monet.exportGeneLegend(
        repDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
        PT_IMG+'/legend_{}.png'.format(AOI), 500
    )
