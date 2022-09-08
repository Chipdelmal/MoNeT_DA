#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import PGS_aux as aux
import PGS_gene as drv
from datetime import datetime
import MoNeT_MGDrivE as monet
from more_itertools import locate
from joblib import Parallel, delayed
# import warnings
# warnings.filterwarnings("ignore")

if monet.isNotebook():
    (USR, DRV, AOI) = ('srv', 'PGS', 'HLT')
else:
    (USR, DRV, AOI) = sys.argv[1:]
GRID_REF = False
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, fldr)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_DTA, PT_PRE, tS, 'PstFraction [{}:{}:{}]'.format(aux.XP_ID, fldr, AOI)
)
###########################################################################
# Base experiments
#   These are the experiments without any releases (for fractions)
###########################################################################
# Get releases number set -------------------------------------------------
ren = aux.getExperimentsIDSets(PT_PRE, skip=-1)[1]
# Get base experiments pattern --------------------------------------------
if GRID_REF:
    basePat = aux.patternForReleases(aux.NO_REL_PAT, AOI, 'sum')
    baseFiles = sorted(glob(PT_PRE+basePat))
    baseFNum = len(baseFiles)
###########################################################################
# Probe experiments
#   sum: Analyzed data aggregated into one node
#   srp: Garbage data aggregated into one node
###########################################################################
(xpNum, digs) = monet.lenAndDigits(ren)
(i, rnIt) = (0, '4')
for (i, rnIt) in enumerate(ren):
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
            aux.replaceExpBase(f, aux.REF_FILE) for f in meanFiles
        ]
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
    # #####################################################################
    # Process data
    # #####################################################################
    Parallel(n_jobs=JOB)(
        delayed(monet.pstFractionParallel)(
            exIx, PT_OUT
        ) for exIx in expIter
    )

