#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
from more_itertools import locate
import GOP_aux as aux
import GOP_gene as drv


if monet.isNotebook():
    (USR, LND, DRV, AOI, SPE) = ('dsk', 'Brikama', 'HUM', 'MRT', 'None')
else:
    (USR, LND, DRV, AOI, SPE) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
(NH, NM) = aux.getPops(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=NM, humSize=NH),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, LND, DRV, SPE
)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_DTA, PT_DTA, tS, 
    '{} PreProcessEpi [{}:{}:{}]'.format(aux.XP_ID, fldr, LND, AOI)
)
# Select sexes and ids --------------------------------------------------------
sexID = {"male": "", "female": "H_"}
###########################################################################
# Load folders
###########################################################################
fmtStr = '{}* Create files list...{}'
print(fmtStr.format(monet.CBBL, monet.CEND), end='\r')
(expDirsMean, expDirsTrac) = monet.getExpPaths(
    PT_DTA, mean='ANALYZED/', reps='TRACE/'
)
(expNum, nodeDigits) = (len(expDirsMean), 2)
expIter = list(zip(list(range(expNum)), expDirsMean, expDirsTrac))
# Check for potential miss-matches in experiments folders -----------------
(meanFNum, tracFNum) = (len(expDirsMean), len(expDirsTrac))
if (meanFNum != tracFNum):
    errorString = 'Unequal experiments folders lengths ({}/{})'
    sys.exit(errorString.format(meanFNum, tracFNum)) 
# Check for pre-existing files and skip if needed -------------------------
if aux.OVW == False:
    expIDPreDone = set(monet.splitExpNames(PT_PRE))
    expIDForProcessing = [i.split('/')[-1] for i in expDirsMean]
    expsIxList = list(locate(
        [(i in expIDPreDone) for i in expIDForProcessing],
        lambda x: x!=True
    ))
    expIter = [expIter[i] for i in expsIxList]
sys.stdout.write("\033[K")
###########################################################################
# Process data
###########################################################################
Parallel(n_jobs=JOB)(
    delayed(monet.preProcessParallel)(
        exIx, expNum, gene,
        analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
        fNameFmt='{}/{}-{}_', MF=(False, True),
        cmpr='bz2', nodeDigits=2,
        SUM=aux.SUM, AGG=aux.AGG, SPA=aux.SPA,
        REP=aux.REP, SRP=aux.SRP,
        sexFilenameIdentifiers=sexID
    ) for exIx in expIter
)

