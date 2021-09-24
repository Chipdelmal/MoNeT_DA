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
    (USR, SET, DRV, AOI) = ('dsk', 'homing', 'ASD', 'TRS')
else:
    (USR, SET, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
###############################################################################
XP_NPAT = aux.XP_HOM
if SET == 'homing':
    XP_NPAT = aux.XP_SHR
###############################################################################
EXPS = aux.EXPS
exp = EXPS[0]
for exp in EXPS:
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=11000),
        lnd.landSelector('SPA')
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, exp
    )
    tS = datetime.now()
    monet.printExperimentHead(
        PT_DTA, PT_OUT, tS, 
        aux.XP_ID+' PstFraction [{}:{}:{}]'.format(DRV, exp, AOI)
    )
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
            repsRatios = monet.getPopRepsRatios(base, trace, 1)
            np.save(fName, repsRatios)

# exp = 'E_099_099_007_000_100_0000001_0000001_12-HLT_00_rto.npy'
# PTH = '/Volumes/marshallShare/yLinked2/shredder/autosomal/001/POSTPROCESS/'
# pop = np.load(PTH+exp)
# tmp = [np.where(i<0.01)[0] for i in pop]
# np.mean(
#     (np.asanyarray([i[0] for i in tmp if (i.shape[0]!=0)])-12*7)/7
# )

# rat = [np.where(i[12*7:]>0.95)[0] for i in pop]
# np.mean(
#     (np.asanyarray([i[0] for i in rat if (i.shape[0]!=0)])-12*7)/7
# )