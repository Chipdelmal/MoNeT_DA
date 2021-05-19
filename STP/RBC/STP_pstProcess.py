#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg


if monet.isNotebook():
    (USR, AOI, LND, QNT) = ('dsk', 'HLT', 'PAN', '50')
    JOB = aux.JOB_DSK
else:
    (USR, AOI, LND, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    JOB = aux.JOB_SRV
(EXPS, DRV) = (aux.getExps(LND), 'LDR')
DF_SORT = ['TTI', 'TTO', 'WOP', 'RAP', 'MIN', 'POE', 'CPT']
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
        lnd.landSelector(exp, LND)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, LND
    )
    ###########################################################################
    # Setting up paths
    ###########################################################################
    tS = datetime.now()
    monet.printExperimentHead(
        PT_OUT, PT_MTR, tS, 
        aux.XP_ID+'  PstProcess [{}:{}:{}]'.format(DRV, exp, AOI)
    )
    ###########################################################################
    # Setup schemes
    ###########################################################################
    pth = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
    DFOPths = [pth.format(z) for z in aux.DATA_NAMES]
    # Setup experiments IDs ---------------------------------------------------
    uids = aux.getExperimentsIDSets(PT_OUT, skip=-1)
    (xpDict, smryDicts) = ({}, [{} for _ in range(len(aux.DATA_NAMES))])
    # Get experiment files ----------------------------------------------------
    ptrn = aux.patternForReleases('*', AOI, 'rto', 'npy')
    fPaths = sorted(glob(PT_OUT+ptrn))
    (fNum, digs) = monet.lenAndDigits(fPaths)
    qnt = float(int(QNT)/100)
    # Setup dataframes --------------------------------------------------------
    outDFs = monet.initDFsForDA(
        fPaths, header, 
        aux.THI, aux.THO, aux.THW, aux.TAP, 
        POE=True, CPT=True
    )
    (ttiDF, ttoDF, wopDF, tapDF, rapDF, poeDF, cptDF, _) = outDFs
    outDFs = (ttiDF, ttoDF, wopDF, tapDF, rapDF, poeDF, cptDF)
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    fmtStr = '{}+ File: {}/{}'
    (i, fPath) = (0, fPaths[0])
    for (i, fPath) in enumerate(fPaths):
        repRto = np.load(fPath)
        # (reps, days) = repRto.shape
        print(
            fmtStr.format(monet.CBBL, str(i+1).zfill(digs), fNum, monet.CEND), 
            end='\r'
        )
        #######################################################################
        # Calculate Metrics
        #######################################################################
        mtrsReps = dbg.calcMetrics(
            repRto, thi=aux.THI, tho=aux.THO, thw=aux.THW, tap=aux.TAP
        )
        #######################################################################
        # Calculate Quantiles
        #######################################################################
        mtrsQnt = dbg.calcMtrQnts(mtrsReps, qnt)
        #######################################################################
        # Update in Dataframes
        #######################################################################
        (xpid, mtrs) = (
            monet.getXpId(fPath, xpidIx),
            [mtrsQnt[k] for k in DF_SORT]
        )
        updates = [xpid+i for i in mtrs]
        for df in zip(outDFs, updates):
            df[0].iloc[i] = df[1]
        #######################################################################
        # Update in Dictionaries
        #######################################################################
        if aux.MLR:
            outDict = [
                    {int(i[0]*100): i[1] for i in zip(aux.THI, ttiS)},
                    {int(i[0]*100): i[1] for i in zip(aux.THO, ttoS)},
                    {int(i[0]*100): i[1] for i in zip(aux.THW, wopS)},
                    {int(i[0]*100): i[1] for i in zip(aux.TAP, rapS)},
                    {
                        'mnl': minS[0], 'mnd': minS[1],
                        'mxl': maxS[0], 'mxd': maxS[1]
                    },
                    {'POE': poe}, {'CPT': cpt}
                ]
            for dct in zip(smryDicts, outDict):
                dct[0][tuple(xpid)] = dct[1]
    ###########################################################################
    # Export Data
    ###########################################################################
    for df in zip(outDFs, DFOPths):
        df[0].to_csv(df[1], index=False)
    if aux.MLR:
        for (i, dicts) in enumerate(smryDicts):
            lbl = aux.DATA_NAMES[i]
            pth = PT_MTR+AOI+'_'+lbl+'_'+QNT+'_mlr.bz'
            pkl.dump(dicts, pth, compression='bz2')

