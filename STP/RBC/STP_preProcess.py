#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
from more_itertools import locate
# os.system("taskset -p 0xff %d" % os.getpid())

if monet.isNotebook():
    (USR, AOI, LND) = ('dsk', 'HLT', 'PAN')
    JOB = aux.JOB_DSK
else:
    (USR, AOI, LND) = (sys.argv[1], sys.argv[2], sys.argv[3])
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
        drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
        lnd.landSelector(exp, LND)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, LND
    )
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_DTA, PT_PRE, tS, 
        '{} PreProcess [{}:{}:{}]'.format(aux.XP_ID, aux.DRV, exp, AOI)
    )
    ###########################################################################
    # Load folders
    ###########################################################################
    (expDirsMean, expDirsTrac) = monet.getExpPaths(
        PT_DTA, mean='ANALYZED/', reps='TRACE/'
    )
    (expNum, nodeDigits) = (len(expDirsMean), len(str(len(land)))+1)
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
        expIter = [xpIter[i] for i in expsIxList]
    ###########################################################################
    # Process data
    ###########################################################################
    Parallel(n_jobs=JOB)(
        delayed(dbg.preProcessParallel)(
            exIx, expNum, gene,
            analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
            fNameFmt='{}/{}-{}_', MF=drv.maleFemaleSelector(AOI),
            cmpr='bz2', nodeDigits=nodeDigits,
            SUM=aux.SUM, AGG=aux.AGG, SPA=aux.SPA,
            REP=aux.REP, SRP=aux.SRP
        ) for exIx in expIter
    )
