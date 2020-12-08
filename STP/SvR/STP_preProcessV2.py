
#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_functions as fun
import STP_preProcessDevFun as deb
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed


# (USR, AOI, REL, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# (USR, AOI, REL, LND, MGV) = ('srv', 'HLT', 'mixed', 'PAN', 'v1')
(USR, AOI, REL, LND, MGV) = ('srv', 'HLT', 'male', 'EPI', 'v2')
(DRV, FMT, OVW, MF, JOB) = ('LDR', 'bz2', True, (True, True), 8)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, False)
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
if MGV == 'v2':
    (expDirsMean, expDirsTrac) = monet.getExpPaths(
        PT_DTA, mean='analyzed/', reps='traces/'
    )
else:
    (expDirsMean, expDirsTrac) = monet.getExpPaths(
        PT_DTA, mean='ANALYZED/', reps='GARBAGE/'
    )
# Split experiment ID ---------------------------------------------------------
(expNum, nodeDigits) = (len(expDirsMean), len(str(len(land)))+1)
outNames = fun.splitExpNames(PT_OUT)
outExpNames = set(outNames)
###############################################################################
# Analyze data
###############################################################################
exIx = 0
monet.preProcess(
        exIx, expNum, expDirsMean, expDirsTrac, gene,
        analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
        outExpNames=outExpNames, fNameFmt='{}{}-{}_', OVW=OVW,
        MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
        SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP,
        sexFilenameIdentifiers={"male": "M_", "female": "F_"}
    ) 
