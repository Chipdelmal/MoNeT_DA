#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import tGD_aux as aux
import tGD_gene as drv
import tGD_fun as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed

###############################################################################
# Drives: LinkedDrive, splitDrive, tGD
###############################################################################
if monet.isNotebook():
    (USR, DRV, AOI) = ('srv3', 'linkedDrive', 'HLT')
else:
    (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(FMT, OVW, JOB) = ('bz2', True, 25)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
EXP = aux.EXPS
NOI = [[0], ]
# Sex selector ----------------------------------------------------------------
if (AOI=='HLT') or (AOI=='CST'):
    MF = (False, True)
else:
    MF = (True, True)
###############################################################################
# Setting up paths and style
###############################################################################
exp = '100'
for exp in EXP:
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
    drive = drv.driveSelector(DRV, AOI)
    DVP = drive.get('gDict')
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    aux.printExperimentHead(PT_DTA, PT_IMG, PT_PRE, tS, 'PreProcess ' + AOI)
    ###########################################################################
    # Load folders
    ###########################################################################
    (expDirsMean, expDirsTrac) = fun.getExpPaths(PT_DTA)
    (expNum, nodeDigits) = (len(expDirsMean), len(str(len(NOI)))+1)
    outNames = fun.splitExpNames(PT_OUT)
    outExpNames = set(outNames)
    ###########################################################################
    # Analyze data
    ###########################################################################
    Parallel(n_jobs=JOB)(
        delayed(monet.preProcess)(
            exIx, expNum, expDirsMean, expDirsTrac, DVP,
            analysisOI=AOI, prePath=PT_PRE, nodesAggLst=NOI,
            outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
            MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
            SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
        ) for exIx in range(0, expNum)
    )
