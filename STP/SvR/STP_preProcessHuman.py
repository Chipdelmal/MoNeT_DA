#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_functions as fun
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed


# (USR, AOI, REL, LND, MGV) = (sys.argv[1], 'HUM', sys.argv[3], sys.argv[4]. sys.argv[5])
(USR, AOI, REL, LND, MGV) = ('dsk', 'HUM', 'male', 'EPI', 'v2')
(DRV, FMT, OVW, MF, JOB) = (AOI, 'bz2', True, (True, False), 4)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=10000), lnd.landSelector(LND)
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_ROT, PT_PRE, tS, 'UCIMI Preprocess '+AOI)
###############################################################################
# Load folders
###############################################################################
(expDirsMean, expDirsTrac) = aux.selectVersionPath(MGV, PT_DTA)
(expNum, nodeDigits) = (len(expDirsMean), len(str(len(land)))+1)
outNames = fun.splitExpNames(PT_OUT)
outExpNames = set(outNames)
###############################################################################
# Analyze data
###############################################################################
Parallel(n_jobs=JOB)(
    delayed(monet.preProcess)(
        exIx, expNum, expDirsMean, expDirsTrac, gene,
        analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
        outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
        MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
        SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP,
        sexFilenameIdentifiers={"male": "H_", "female": "_"}
    ) for exIx in range(0, expNum)
)
