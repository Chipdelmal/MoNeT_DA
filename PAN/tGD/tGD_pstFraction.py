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
from more_itertools import locate
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet

if monet.isNotebook():
    (USR, DRV, AOI, QNT) = ('srv', 'linkedDrive', 'HLT', '50')
else:
    (USR, DRV, AOI, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
(SKP, OVW) = (False, True)
exp = '100'
GRID_REF = False
JOB = 20
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
(i, rnIt) = (0, ren[1])
for (i, rnIt) in enumerate(ren[1:]):
    monet.printProgress(i+1, xpNum, digs)
    # Repetitions data (Garbage) ------------------------------------------
    tracePat = aux.patternForReleases(rnIt, AOI, 'srp', pad=aux.DATA_PAD['i_ren'])
    traceFiles = sorted(glob(PT_PRE+tracePat))
    # Mean data (Analyzed) ------------------------------------------------
    meanPat = aux.patternForReleases(rnIt, AOI, 'sum', pad=aux.DATA_PAD['i_ren'])
    meanFiles = sorted(glob(PT_PRE+meanPat))
    expNum = len(meanFiles)
    # Patch for static reference file -------------------------------------
    if not GRID_REF:
        baseFiles = [
            PT_PRE+f"/E_000000_000000_000000_000000_000000_000000_00_0000-{AOI}_00_sum.bz"
        ]*expNum
        baseFNum = len(baseFiles)
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
    ###########################################################################
    # Process data
    ###########################################################################
    Parallel(n_jobs=JOB)(
        delayed(monet.pstFractionParallel)(
            exIx, PT_OUT
        ) for exIx in expIter
    )
