#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
from more_itertools import locate
from joblib import Parallel, delayed


if monet.isNotebook():
    (USR, AOI, LND) = ('dsk', 'HLT', 'PAN')
    JOB = aux.JOB_DSK
else:
    (USR, AOI, LND) = (sys.argv[1], sys.argv[2], sys.argv[3])
    JOB = aux.JOB_SRV
(EXPS, DRV) = (aux.getExps(LND), 'LDR')
###############################################################################
# Processing loop
###############################################################################
exp = EXPS[0]
for exp in EXPS:
    # #########################################################################
    # Setup paths and drive
    # #########################################################################
    (drive, land) = (
        drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
        lnd.landSelector(exp, LND)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, LND
    )
    tS = datetime.now()
    monet.printExperimentHead(
        PT_PRE, PT_OUT, tS, 
        aux.XP_ID+' PstFraction [{}:{}:{}]'.format(aux.DRV, exp, AOI)
    )
    # #########################################################################
    # Base experiments
    #   These are the experiments without any releases (for fractions)
    # #########################################################################
    # Get releases number set -------------------------------------------------
    ren = aux.getExperimentsIDSets(PT_PRE, skip=-1)[2]
    # Get base experiments pattern --------------------------------------------
    basePat = aux.patternForReleases(aux.NO_REL_PAT, AOI, 'sum')
    baseFiles = sorted(glob(PT_PRE+basePat))
    baseFNum = len(baseFiles)
    # #########################################################################
    # Probe experiments
    #   sum: Analyzed data aggregated into one node
    #   srp: Garbage data aggregated into one node
    # #########################################################################
    (xpNum, digs) = monet.lenAndDigits(ren)
    (i, rnIt) = (0, '00')
    for (i, rnIt) in enumerate(ren):
        monet.printProgress(i+1, xpNum, digs)
        # Mean data (Analyzed) ------------------------------------------------
        meanPat = aux.patternForReleases(rnIt, AOI, 'sum')
        meanFiles = sorted(glob(PT_PRE+meanPat))
        expNum = len(meanFiles)
        # Repetitions data (Garbage) ------------------------------------------
        tracePat = aux.patternForReleases(rnIt, AOI, 'srp')
        traceFiles = sorted(glob(PT_PRE+tracePat))
        # Create experiments iterator list ------------------------------------
        expIter = list(zip(
            list(range(expNum)), baseFiles, meanFiles, traceFiles
        ))
        # Check for potential miss-matches in experiments folders -------------
        (meanFNum, tracFNum) = (len(meanFiles), len(traceFiles))
        if (meanFNum!=tracFNum) or (baseFNum!=meanFNum) or (baseFNum!=tracFNum):
            errorString = 'Unequal experiments folders lengths ({}/{}/{})'
            sys.exit(errorString.format(baseFNum, meanFNum, tracFNum)) 
        # Filter existing if needed -------------------------------------------
        if aux.OVW == False:
            expIDPreDone = set(monet.splitExpNames(PT_OUT, ext='npy'))
            expIDForProcessing = [i.split('/')[-1][:-14] for i in meanFiles]
            expsIxList = list(locate(
                [(i in expIDPreDone) for i in expIDForProcessing], 
                lambda x: x!=True
            ))
            expIter = [expIter[i] for i in expsIxList]
        # #####################################################################
        # Process data
        # #####################################################################
        Parallel(n_jobs=JOB)(
            delayed(dbg.pstFractionParallel)(
                exIx, PT_OUT
            ) for exIx in expIter
        )
