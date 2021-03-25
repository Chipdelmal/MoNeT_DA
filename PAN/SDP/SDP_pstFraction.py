#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import SDP_aux as aux
import SDP_land as lnd
import SDP_gene as drv


if monet.isNotebook():
    (USR, DRV, AOI) = ('dsk', 'CRS', 'HLT')
else:
    (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
###############################################################################
(gIx, hIx) = (1, 0)
EXPS = ('000', '001', '010')
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=25e3), lnd.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
###############################################################################
exp = EXPS[0]
for exp in EXPS:
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, fldr, exp
    )
    tS = datetime.now()
    monet.printExperimentHead(PT_PRE, PT_OUT, tS, 'SDP PstFraction '+AOI)
    ###############################################################################
    # Setting up paths and style
    ###############################################################################
    uids = aux.getExperimentsIDSets(PT_PRE, skip=-1, ext='.bz')
    (par, csa, csb, ren, res, aoi, grp) = uids[1:]
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
