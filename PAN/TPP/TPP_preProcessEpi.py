#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from joblib import Parallel, delayed
from more_itertools import locate
import MoNeT_MGDrivE as monet
import TPP_aux as aux
import TPP_gene as drv

if monet.isNotebook():
    (USR, LND, EXP, DRV, AOI) = (
        'zelda', 'BurkinaFaso', 'highEIR', 'HUM', 'PRV'
    )
else:
    (USR, LND, EXP, DRV, AOI) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'zelda':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
(NH, NM) = aux.getPops(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, EXP)
# Time and head -----------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_DTA, PT_PRE, tS, 'PreProcess [{}:{}:{}]'.format(aux.XP_ID, fldr, AOI)
)
# Select sexes and ids --------------------------------------------------------
sexID = {"male": "", "female": "H_"}
###########################################################################
# Load folders
###########################################################################
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
###########################################################################
# Process data
###########################################################################
Parallel(n_jobs=JOB)(
    delayed(monet.preProcessParallel)(
        exIx, expNum, gene,
        analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
        fNameFmt='{}/{}-{}_', MF=(False, True),
        cmpr='bz2', nodeDigits=2,
        SUM=aux.SUM, AGG=aux.AGG, SPA=aux.SPA,
        REP=aux.REP, SRP=aux.SRP,
        sexFilenameIdentifiers=sexID
    ) for exIx in expIter
)

# fName = 'E_26_07000_0075000-MRT_00_sum'
# dta = pkl.load(path.join(PT_PRE, fName+'.bz'))
# print(dta)