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
    (USR, AOI, DRV, QNT, THS, SPE) = ('dsk', 'HUM', 'INC', 50, 0.1, 'gambiae_0_low')
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
    # tS = datetime.now()
    # monet.printExperimentHead(
    #     PT_OUT, PT_IMG, tS, 
    #     aux.XP_ID+' PstTraces [{}:{}:{}]'.format(DRV, exp, AOI)
    # )
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
    # Check TTI
    ttis = [round((dfTTI.iloc[-1][i]-aux.RELEASES[-1])/30, 2) for i in ('0.9', '0.5', '0.1')]
    print(SPE, exp, ttis)
    