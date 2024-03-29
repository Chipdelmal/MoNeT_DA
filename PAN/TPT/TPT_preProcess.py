#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from os import path
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
from joblib import Parallel, delayed
from more_itertools import locate
import TPT_aux as aux
import TPT_gene as drv
import TPT_functions as fun

if monet.isNotebook():
    (USR, AOI, DRV, SPE) = ('srv', 'HUM', 'LDR', 'coluzzii_10_low')
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
    tS = datetime.now()
    monet.printExperimentHead(
        PT_DTA, PT_PRE, tS, 
        '{} PreProcess [{}:{}:{}]'.format(aux.XP_ID, fldr, exp, AOI)
    )
    # Select sexes and ids ----------------------------------------------------
    if (AOI == 'HUM'):
        sexID = {"male": "H_", "female": "H_"}
    elif (AOI == 'INC'):
        sexID = {"male": "incidence_", "female": "incidence_"}
        exclusionPattern = lambda a: len(a.split('/')[-1]) >= 18
    else:
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
###############################################################################
# Explore
###############################################################################
# pth = '/RAID5/marshallShare/TP13_figure_gambiae_low/X2500/PREPROCESS'
# exp = 'E_00_00000_00000000000_000000000000_0000000_0000000_0000000_0000000_0000000-INC_00_rto.npy'
# exp = "E_15_00500_00400000000_000100000000_0017500_0011700_0000000_0089000_0089000-INC_00_sum.bz"
# raw = pkl.load(path.join(pth, exp))
# max(raw['population'].T[1])

