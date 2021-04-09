#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed

if monet.isNotebook():
    (USR, AOI, EXP, LND) = ('dsk', 'HLT', 'PAN', 'PAN')
    (OVW, JOB) = (True, aux.JOB_DSK)
else:
    (USR, AOI, EXP, LND) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    )
    (OVW, JOB) = (True, aux.JOB_SRV)
###########################################################################
# Setting up paths
###########################################################################
(drive, land) = (
    drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE), 
    lnd.landSelector(EXP, LND)
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, EXP, LND
)
# Time and head -----------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_DTA, PT_PRE, tS, 
    aux.XP_ID+' PreProcess [{}:{}:{}]'.format(aux.DRV, EXP, AOI)
)
###########################################################################
# Load folders
###########################################################################
(expDirsMean, expDirsTrac) = monet.getExpPaths(
    PT_DTA, mean='ANALYZED/', reps='TRACES/'
)
(expNum, nodeDigits) = (len(expDirsMean), len(str(len(land)))+1)
outNames = monet.splitExpNames(PT_OUT)
outExpNames = set(outNames)
###########################################################################
# Process data
###########################################################################
Parallel(n_jobs=1)(
    delayed(monet.preProcess)(
            exIx, expNum, expDirsMean, expDirsTrac, gene,
            analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
            outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
            MF=drv.maleFemaleSelector(AOI), 
            cmpr='bz2', nodeDigits=nodeDigits,
            SUM=aux.SUM, AGG=aux.AGG, SPA=aux.SPA,
            REP=aux.REP, SRP=aux.SRP
    ) for exIx in range(0, expNum)
)
