#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet

if monet.isNotebook():
    (USR, SET, DRV, AOI) = ('dsk', 'homing', 'ASD', 'HLT')
else:
    (USR, SET, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
(FMT, OVW) = ('bz2', True)
(gIx, hIx) = (1, 0)
###############################################################################
EXPS = ('000', '002', '004', '006', '008')
# Homing or shredder pattern-matching -----------------------------------------
XP_NPAT = aux.XP_HOM
if SET == 'homing':
    XP_NPAT = aux.XP_SHR
###############################################################################
for EXP in EXPS:
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=11000),
        lnd.landSelector('SPA')
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, EXP
    )
    tS = datetime.now()
    monet.printExperimentHead(PT_DTA, PT_OUT, tS, 'PstFraction '+AOI)
    # #########################################################################
    # Base experiments
    #   These are the experiments without any releases (for fractions)
    # #########################################################################
    # Get releases number set -------------------------------------------------
    ren = aux.getExperimentsIDSets(PT_PRE, skip=-1)[-3]
    # Get base experiments pattern --------------------------------------------
    basePat = aux.patternForReleases(SET, '00', AOI, 'sum')
    baseFiles = sorted(glob(PT_PRE+basePat))
    # #########################################################################
    # Probe experiments
    #   sum: Analyzed data aggregated into one node
    #   srp: Garbage data aggregated into one node
    # #########################################################################
    (xpNum, digs) = monet.lenAndDigits(ren)
    for (i, rnIt) in enumerate(ren):
        monet.printProgress(i+1, xpNum, digs)
        # Mean data (Analyzed) ------------------------------------------------
        meanPat = aux.patternForReleases(SET, rnIt, AOI, 'sum')
        meanFiles = sorted(glob(PT_PRE+meanPat))
        # Repetitions data (Garbage) ------------------------------------------
        tracePat = aux.patternForReleases(SET, rnIt, AOI, 'srp')
        traceFiles = sorted(glob(PT_PRE+tracePat))
        # #####################################################################
        # Load data
        # #####################################################################
        expNum = len(meanFiles)
        for pIx in range(expNum):
            (bFile, mFile, tFile) = (baseFiles[pIx], meanFiles[pIx], traceFiles[pIx])
            (base, mean, trace) = [pkl.load(file) for file in (bFile, mFile, tFile)]
            # #################################################################
            # Process data
            # #################################################################
            fName = '{}{}rto'.format(PT_OUT, mFile.split('/')[-1][:-6])
            repsRatios = monet.getPopRepsRatios(base, trace, gIx)
            np.save(fName, repsRatios)
