
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import v2_aux as aux
import v2_gene as drv
# import v2_land as lnd
# import v2_functions as fun
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed


if monet.isNotebook():
    (USR, DRV, AOI) = ('dsk', 'SDR', 'HLT')
else:
    (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
###############################################################################
(FMT, OVW, JOB, MF) = ('bz2', False, 4, (True, True))
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
###############################################################################
# Setting up paths and drive
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR)
(expDirsMean, expDirsTrac) = monet.getExpPaths(
    PT_DTA, mean='analyzed/', reps='traces/'
)
(drive, land) = (drv.driveSelector(DRV, AOI, popSize=10*10000), ([0], ))
MF = (True, True)
if AOI == 'HLT':
    MF = (False, True)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_ROT, PT_PRE, tS, 'V2 Preprocess '+AOI)
###############################################################################
# Load folders
###############################################################################
(expNum, nodeDigits) = (len(expDirsMean), len(str(len(land)))+1)
###############################################################################
# Analyze data
###############################################################################
Parallel(n_jobs=JOB)(
    delayed(monet.preProcess)(
        exIx, expNum, expDirsMean, expDirsTrac, gene,
        analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
        outExpNames=(None, ), fNameFmt='{}/{}-{}_', OVW=OVW,
        MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
        SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP,
        sexFilenameIdentifiers={"male": "M_", "female": "F_"}
    ) for exIx in range(0, expNum)
)