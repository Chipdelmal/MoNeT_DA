#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
from more_itertools import locate
import TPT_aux as aux
import TPT_gene as drv


if monet.isNotebook():
    (USR, DRV, AOI) = ('dsk', 'LDR', 'INC')
else:
    USR = sys.argv[1]
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
        USR, exp, DRV
    )
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_DTA, PT_PRE, tS, 
        '{} PreProcess [{}:{}:{}]'.format(aux.XP_ID, fldr, exp, AOI)
    )
    # Select sexes and ids ----------------------------------------------------
    sexID = {"male": "M_", "female": "F_"}
    if (AOI == 'HUM'):
        sexID = {"male": "", "female": "H_"}
    elif (AOI == 'INC'):
        sexID == {"male": "", "female": "incidence_"}
    ###########################################################################
    # Load folders
    ###########################################################################
    fmtStr = '{}* Create files list...{}'
    print(fmtStr.format(monet.CBBL, monet.CEND), end='\r')
    (expDirsMean, expDirsTrac) = monet.getExpPaths(
        PT_DTA, mean='ANALYZED/', reps='TRACE/'
    )