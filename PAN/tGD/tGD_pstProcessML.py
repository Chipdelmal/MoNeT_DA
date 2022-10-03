#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from glob import glob
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
from more_itertools import locate
import pandas as pd
import compress_pickle as pkl
import tGD_aux as aux
import tGD_gene as drv


if monet.isNotebook():
    (USR, DRV, AOI, QNT) = ('srv', 'linkedDrive', 'HLT', '50')
else:
    (USR, DRV, AOI, QNT) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###############################################################################
# Get Experiments and Offset
###############################################################################
EXPS = aux.EXPS
###############################################################################
# Processing loop
###############################################################################
exp = EXPS[0]
(header, xpidIx) = list(zip(*aux.DATA_HEAD))
###########################################################################
# Load landscape and drive
###########################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    [[0], ]
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
# PT_OUT_ML = PT_OUT.replace('/100', '')
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_DTA, PT_OUT, tS, 'PstProcessML [{}:{}:{}]'.format(
        DRV, fldr, AOI
    )
)
###########################################################################
# Setup schemes
###########################################################################
# pth = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
pth = PT_MTR+AOI+'_{}_MLR'
DFOPths = [pth.format(z) for z in aux.DATA_NAMES]
# Setup experiments IDs ---------------------------------------------------
uids = aux.getExperimentsIDSets(PT_OUT, skip=-1)
# Get experiment files ----------------------------------------------------
ptrn = aux.patternForReleases('*', AOI, 'rto', 'npy')
fPaths = sorted(glob(PT_OUT+ptrn))
qnt = float(int(QNT)/100)
###########################################################################
# Divide fPaths in chunks
###########################################################################
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
###########################################################################
# Merge dataframes chunks
###########################################################################
dfPathsPieces = list(zip(*dfPaths))[:]
dfPathsPieces = [dfPathsPieces[i] for i in (0, 1, 2, 4, 6)]
dfPathsSet = dfPathsPieces[0]
for dfPathsSet in dfPathsPieces:
    dfFull = pd.concat([pd.read_csv(i) for i in dfPathsSet])
    # Write combined dataframe --------------------------------------------
    # pName = dfPathsSet[0].replace('/100/SUMMARY', '/ML')
    #fName = pName.split('-')[0]+'.csv'
    fName = dfPathsSet[0].split('-')[0]+'.csv'
    dfFull.to_csv(fName, index=False)

