#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from joblib import Parallel, delayed
from more_itertools import locate
import MoNeT_MGDrivE as monet
import FMS_aux as aux
import FMS_gene as drv

if monet.isNotebook():
    (USR, DRV, AOI) = ('lab', 'FMS', 'ECO')
else:
    (USR, DRV, AOI) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE, humSize=aux.HUM_SIZE),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, fldr)
# Time and head -----------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_DTA, PT_PRE, tS, 'PreProcess [{}:{}:{}]'.format(aux.XP_ID, fldr, AOI)
)
# Select sexes and ids ----------------------------------------------------
sexID = {"male": "M_", "female": "F_"}
###########################################################################
# Load folders
###########################################################################
fmtStr = '{}* Create files list...{}'
print(fmtStr.format(monet.CBBL, monet.CEND), end='\r')
(expDirsMean, expDirsTrac) = monet.getExpPaths(
    PT_DTA, mean='ANALYZED/', reps='TRACE/'
)
(expNum, nodeDigits) = (len(expDirsMean), 2)
expIter = list(zip(list(range(expNum)), expDirsMean, expDirsTrac))
# Check for potential miss-matches in experiments folders -----------------
(meanFNum, tracFNum) = (len(expDirsMean), len(expDirsTrac))
if (meanFNum != tracFNum):
    errorString = 'Unequal experiments folders lengths ({}/{})'
    sys.exit(errorString.format(meanFNum, tracFNum)) 
# Check for pre-existing files and skip if needed -------------------------
if aux.OVW == False:
    expIDPreDone = set(monet.splitExpNames(PT_PRE))
    expIDForProcessing = [i.split('/')[-1] for i in expDirsMean]
    expsIxList = list(locate(
        [(i in expIDPreDone) for i in expIDForProcessing],
        lambda x: x!=True
    ))
    expIter = [expIter[i] for i in expsIxList]
sys.stdout.write("\033[K")
###########################################################################
# Process data
###########################################################################
Parallel(n_jobs=JOB)(
    delayed(monet.preProcessParallel)(
        exIx, expNum, gene,
        analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
        fNameFmt='{}/{}-{}_', MF=drv.maleFemaleSelector(AOI),
        cmpr='bz2', nodeDigits=2,
        SUM=aux.SUM, AGG=aux.AGG, SPA=aux.SPA,
        REP=aux.REP, SRP=aux.SRP,
        sexFilenameIdentifiers=sexID
    ) for exIx in expIter
)
