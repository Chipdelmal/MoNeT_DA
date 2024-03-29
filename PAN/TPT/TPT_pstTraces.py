#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from glob import glob
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
from more_itertools import locate
import compress_pickle as pkl
import pandas as pd
import TPT_aux as aux
import TPT_gene as drv
import TPT_functions as fun

if monet.isNotebook():
    (USR, AOI, DRV, QNT, THS, SPE) = ('dsk', 'HUM', 'LDR', 50, 0.1, 'coluzzii_10_med')
else:
    (USR, AOI, DRV, QNT, THS, SPE) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###############################################################################
# Get Experiments and Offset
###############################################################################
(EXPS, REL_START) = (aux.getExps(), aux.landSelector(USR=USR))
###############################################################################
# Processing loop
###############################################################################
exp = EXPS[2]
for exp in EXPS:
    (header, xpidIx) = list(zip(*aux.DATA_HEAD))
    ###########################################################################
    # Load landscape and drive
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE, humSize=aux.HUM_SIZE),
        aux.landSelector(USR=USR)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, DRV, SPE
    )
    PT_IMG = PT_IMG + 'pstTraces/'
    monet.makeFolder(PT_IMG)
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_OUT, PT_IMG, tS, 
        aux.XP_ID+' PstTraces [{}:{}:{}]'.format(DRV, exp, AOI)
    )
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .4, "alpha": .75, "dpi": 500, "legend": True,
            "aspect": 1/6, "colors": CLR, 
            "xRange": aux.XRAN, "yRange": [0, YRAN[1]]
        }
    ###########################################################################
    # Load postprocessed files
    ###########################################################################
    ###########################################################################
    pstPat = PT_MTR+AOI+'_{}_'+str(QNT)+'_qnt.csv'
    pstFiles = [pstPat.format(i) for i in aux.DATA_NAMES]
    (dfTTI, dfTTO, dfWOP, dfRAP, dfMNX, dfPOE, dfCPT) = [
        pd.read_csv(i) for i in pstFiles
    ]
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    (fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
    if aux.FZ:
        fltrPattern = aux.patternForReleases('00', AOI, 'srp')
    repFiles = monet.getFilteredFiles(
        PT_PRE+fltrPattern, globPattern.format('srp')
    )
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    wopC = ('#072ac825' if THS=='0.1' else '#3687ff22')
    (fNum, digs) = monet.lenAndDigits(repFiles)
    Parallel(n_jobs=JOB)(
        delayed(fun.exportPstTracesPlotWrapper)(
            exIx, repFiles, xpidIx,
            dfTTI, dfTTO, dfWOP, dfMNX, dfPOE, dfCPT,
            aux.STABLE_T, str(THS), QNT, STYLE, PT_IMG,
            digs=digs, popScaler=1, autoAspect=1,
            border=True, borderColor='#000000AA', borderWidth=1,
            labelPos=(.91, .875), fontsize=5, labelspacing=.08,
            transparent=True, vlines=aux.RELEASES, # +list(range(0, aux.XRAN[-1], 60)), 
            poePrint=False,
            wopPrint=False, cptPrint=False, mnfPrint=False,
            wopColor=wopC
        ) for exIx in range(0, len(repFiles))
    )
    # Export gene legend ------------------------------------------------------
    # repDta = pkl.load(repFiles[-1])
    # monet.exportGeneLegend(
    #     repDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
    #     PT_IMG+'/legend_{}.png'.format(AOI), 500
    # )
