#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet


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
    # #########################################################################
    # Probe experiments
    #   sum: Analyzed data aggregated into one node
    #   srp: Garbage data aggregated into one node
    # #########################################################################
    (xpNum, digs) = monet.lenAndDigits(ren)
    (i, rnIt) = (0, '10')
    for (i, rnIt) in enumerate(ren):
        monet.printProgress(i+1, xpNum, digs)
        # Mean data (Analyzed) ------------------------------------------------
        meanPat = aux.patternForReleases(rnIt, AOI, 'sum')
        meanFiles = sorted(glob(PT_PRE+meanPat))
        # Repetitions data (Garbage) ------------------------------------------
        tracePat = aux.patternForReleases(rnIt, AOI, 'srp')
        traceFiles = sorted(glob(PT_PRE+tracePat))
        # #####################################################################
        # Load data
        # #####################################################################
        expNum = len(meanFiles)
        pIx = 0
        for pIx in range(expNum):
            (bFile, mFile, tFile) = (
                baseFiles[pIx], meanFiles[pIx], traceFiles[pIx]
            )
            (base, mean, trace) = [
                pkl.load(file) for file in (bFile, mFile, tFile)
            ]
            # #################################################################
            # Process data
            # #################################################################
            fName = '{}{}rto'.format(PT_OUT, mFile.split('/')[-1][:-6])
            repsRatios = monet.getPopRepsRatios(base, trace, 1)
            # for i in repsRatios:
            #     for t in range(0, 5):
            #         i[t] = 1
            np.save(fName, repsRatios)