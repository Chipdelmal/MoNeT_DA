#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import PYF_aux as aux
import PYF_gene as drv
import PYF_land as lnd
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet


if monet.isNotebook():
    (USR, DRV, AOI, LND) = ('dsk', 'PGS', 'HLT', 'PAN')
else:
    (USR, DRV, AOI, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
(gIx, hIx, OVW) = (1, 0, True)
###############################################################################
# Setting up paths
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR, PT_MOD) = aux.selectPath(
    USR, LND
)
tS = datetime.now()
monet.printExperimentHead(PT_DTA, PT_OUT, tS, 'PYF PstFraction '+AOI)
###############################################################################
# Load landscape and drive
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=11000),
    lnd.landSelector(LND, PT_ROT)
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
# #########################################################################
# Base experiments
#   These are the experiments without any releases (for fractions)
# #########################################################################
# Get releases number set -------------------------------------------------
ren = aux.getExperimentsIDSets(PT_PRE, skip=-1)[2]
# Get base experiments pattern --------------------------------------------
basePat = aux.patternForReleases('000', AOI, 'sum')
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
    meanPat = aux.patternForReleases(rnIt, AOI, 'sum')
    meanFiles = sorted(glob(PT_PRE+meanPat))
    # Repetitions data (Garbage) ------------------------------------------
    tracePat = aux.patternForReleases(rnIt, AOI, 'srp')
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
