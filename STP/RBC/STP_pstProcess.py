#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from glob import glob
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
from joblib import Parallel, delayed


if monet.isNotebook():
    (USR, AOI, LND, DRV, QNT) = ('lab', 'HLT', 'SPA', 'LDR', '50')
    JOB = aux.JOB_DSK
    CHUNKS = JOB
else:
    (USR, AOI, LND, DRV, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
    JOB = aux.JOB_SRV
    CHUNKS = JOB
###############################################################################
# Get Experiments and Offset
###############################################################################
(EXPS, REL_START) = (aux.getExps(LND), lnd.landRelSelector(LND))
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
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
        lnd.landSelector(exp, LND, USR=USR)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, LND, DRV
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
    fPathsChunks = list(dbg.chunks(fPaths, CHUNKS))
    dfPaths = [
        [pth+'-pt_'+str(ix).zfill(2)+'.csv' 
        for pth in DFOPths] for ix in range(CHUNKS)
    ]
    expIter = list(zip(dfPaths, fPathsChunks))
    Parallel(n_jobs=JOB)(
        delayed(dbg.pstProcessParallel)(
            exIx, header, xpidIx, 
            qnt=qnt, sampRate=aux.SAMP_RATE, offset=0,
            thi=aux.THI, tho=aux.THO, thw=aux.THW, 
            tap=aux.TAP, thp=(.05, .95)
        ) for exIx in expIter
    )
    ###########################################################################
    # Merge dataframes chunks
    ###########################################################################
    dfPathsPieces = list(zip(*dfPaths))[:-1]
    for dfPathsSet in dfPathsPieces:
        dfFull = pd.concat([pd.read_csv(i) for i in dfPathsSet])
        # Write combined dataframe --------------------------------------------
        fName = dfPathsSet[0].split('-')[0]+'.csv'
        dfFull.to_csv(fName, index=False)



