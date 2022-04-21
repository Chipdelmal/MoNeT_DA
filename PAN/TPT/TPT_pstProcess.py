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
import TPT_aux as aux
import TPT_gene as drv


if monet.isNotebook():
    (USR, AOI, DRV, QNT, SPE) = ('dsk', 'HLT', 'LDR', '50', 'gambiae')
else:
    (USR, AOI, DRV, QNT, SPE) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = 1# JOB
###############################################################################
# Get Experiments and Offset
###############################################################################
(EXPS, REL_START) = (aux.getExps(), aux.landSelector(USR=USR))
###############################################################################
# Processing loop
###############################################################################
exp = EXPS[0]
for exp in EXPS:
    (header, xpidIx) = list(zip(*aux.DATA_HEAD))
    ###########################################################################
    # Load landscape and drive
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE, humSize=aux.HUM_SIZE),
        aux.landSelector(USR=USR)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, DRV, SPE
    )
    ###########################################################################
    # Setting up paths
    ###########################################################################
    tS = datetime.now()
    monet.printExperimentHead(
        PT_OUT, PT_MTR, tS, 
        aux.XP_ID+' PstProcess [{}:{}:{}]'.format(DRV, exp, AOI)
    )
    ###########################################################################
    # Setup schemes
    ###########################################################################
    # pth = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
    pth = PT_MTR+AOI+'_{}_'+QNT+'_qnt'
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
    # print(dfPaths)
    expIter = list(zip(dfPaths, fPathsChunks))
    Parallel(n_jobs=JOB)(
        delayed(monet.pstProcessParallel)(
            exIx, header, xpidIx, 
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
    for dfPathsSet in dfPathsPieces:
        dfFull = pd.concat([pd.read_csv(i) for i in dfPathsSet])
        # Write combined dataframe --------------------------------------------
        fName = dfPathsSet[0].split('-')[0]+'.csv'
        dfFull.to_csv(fName, index=False)



