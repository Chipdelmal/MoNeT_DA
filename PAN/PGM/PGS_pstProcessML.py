#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import numpy as np
from glob import glob
import PGS_aux as aux
import PGS_gene as drv
from datetime import datetime
import MoNeT_MGDrivE as monet
from more_itertools import locate
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
# import warnings
# warnings.filterwarnings("ignore")

if monet.isNotebook():
    (USR, DRV, AOI, QNT) = ('srv', 'PGS', 'HLT', '50')
else:
    (USR, DRV, AOI, QNT) = sys.argv[1:]
GRID_REF = False
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
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
    PT_DTA, PT_OUT, tS, 'PstProcessML [{}:{}:{}]'.format(aux.XP_ID, fldr, AOI)
)
###############################################################################
# Processing loop
###############################################################################
(header, xpidIx) = list(zip(*aux.DATA_HEAD))
###############################################################################
# Setup schemes
###############################################################################
# pth = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
pth = PT_MTR+AOI+'_{}_MLR'
DFOPths = [pth.format(z) for z in aux.DATA_NAMES]
# Setup experiments IDs ---------------------------------------------------
uids = aux.getExperimentsIDSets(PT_OUT, skip=-1)
# Get experiment files ----------------------------------------------------
ptrn = aux.patternForReleases('*', AOI, 'rto', 'npy')
fPaths = sorted(glob(PT_OUT+ptrn))
qnt = float(int(QNT)/100)
###############################################################################
# Divide fPaths in chunks
###############################################################################
fPathsChunks = list(aux.chunks(fPaths, CHUNKS))
dfPaths = [
    [pth+'-pt_'+str(ix).zfill(2)+'.csv' 
    for pth in DFOPths] for ix in range(CHUNKS)
]
expIter = list(zip(dfPaths, fPathsChunks))
Parallel(n_jobs=JOB)(
    delayed(monet.pstProcessParallelML)(
        exIx, header, xpidIx, aux.MAX_REPS,
        qnt=qnt, 
        sampRate=aux.SAMP_RATE, # offset=0,
        thi=aux.THI, tho=aux.THO, thw=aux.THW, 
        tap=aux.TAP, thp=(.05, .95)
    ) for exIx in expIter
)
###############################################################################
# Merge dataframes chunks
###############################################################################
dfPathsPieces = list(zip(*dfPaths))[:]
dfPathsPieces = [dfPathsPieces[i] for i in (0, 1, 2, 4, 6)]
for dfPathsSet in dfPathsPieces:
    dfFull = pd.concat([pd.read_csv(i) for i in dfPathsSet])
    # Write combined dataframe --------------------------------------------
    fName = dfPathsSet[0].split('-')[0]+'.csv'
    dfFull.to_csv(fName, index=False)

