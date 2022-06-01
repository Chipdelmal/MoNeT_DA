#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import tGD_aux as aux
# import STP_functions as fun
# import STP_dataProcess as da
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet

if monet.isNotebook():
    (USR, DRV, AOI, QNT) = ('srv', 'linkedDrive', 'HLT', '50')
else:
    (USR, DRV, AOI, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
(SKP, OVW) = (False, True)
exp = '100'
# #########################################################################
# Setup ids and paths
# #########################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
uids = aux.getExperimentsIDSets(PT_PRE, skip=-1)
(fcs, fcb, fga, fgb, cut, hdr, ren, res, aoi, grp) = uids[1:]
tS = datetime.now()
monet.printExperimentHead(PT_PRE, PT_OUT, tS, 'tGD PstFraction '+AOI)
# #########################################################################
# Base experiments
#   These are the experiments without any releases (for fractions)
# #########################################################################
basePat = aux.patternForReleases('00', AOI, 'sum')
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
    # meanPat = aux.XP_NPAT.format('*', rnIt, '*', '*', '*', AOI, '*', 'sum', 'bz')
    meanPat = aux.patternForReleases(rnIt, AOI, 'sum')
    meanFiles = sorted(glob(PT_PRE+meanPat))
    # Repetitions data (Garbage) ------------------------------------------
    # tracePat = aux.XP_NPAT.format('*', rnIt, '*', '*', '*', AOI, '*', 'srp', 'bz')
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
        repsRatios = monet.getPopRepsRatios(base, trace, 1)
        np.save(fName, repsRatios)
