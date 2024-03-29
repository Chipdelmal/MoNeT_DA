#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import SDP_aux as aux
import SDP_gene as drv
import SDP_land as lnd
# import SDP_functions as fun


if monet.isNotebook():
    (USR, DRV, AOI, QNT) = ('zelda', 'PGS', 'HLT', '50')
else:
    (USR, DRV, AOI, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
###############################################################################
# Load landscape and drive
###############################################################################
(header, xpidIx) = list(zip(*aux.DATA_HEAD))
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE), lnd.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
###############################################################################
# Iterate through experiments
###############################################################################
EXPS = aux.EXPS
exp = EXPS[0]
for exp in EXPS:
    ###########################################################################
    # Setting up paths
    ###########################################################################
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, fldr, exp
    )
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
    (ttiDF, ttoDF, wopDF, tapDF, rapDF, poeDF, cptDF, derDF) = outDFs
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    fmtStr = '{}+ File: {}/{}'
    (i, fPath) = (0, fPaths[0])
    for (i, fPath) in enumerate(fPaths):
        repRto = np.load(fPath)
        (reps, days) = repRto.shape
        print(
            fmtStr.format(monet.CBBL, str(i+1).zfill(digs), fNum, monet.CEND)
            , end='\r'
        )
        #######################################################################
        # Calculate Metrics
        #######################################################################
        (ttiS, ttoS, wopS) = (
                monet.calcTTI(repRto, aux.THI),
                monet.calcTTO(repRto, aux.THO),
                monet.calcWOP(repRto, aux.THW)
            )
        (minS, maxS, _, _) = monet.calcMinMax(repRto)
        rapS = monet.getRatioAtTime(repRto, aux.TAP)
        poe = monet.calcPOE(repRto)
        cpt = monet.calcCPT(repRto)
        der = monet.calcDER(repRto, smoothing=10, magnitude=0.1)
        #######################################################################
        # Calculate Quantiles
        #######################################################################
        ttiSQ = [np.nanquantile(tti, qnt) for tti in ttiS]
        ttoSQ = [np.nanquantile(tto, 1-qnt) for tto in ttoS]
        wopSQ = [np.nanquantile(wop, 1-qnt) for wop in wopS]
        rapSQ = [np.nanquantile(rap, qnt) for rap in rapS]
        mniSQ = (np.nanquantile(minS[0], qnt), np.nanquantile(minS[1], qnt))
        mnxSQ = (np.nanquantile(maxS[0], qnt), np.nanquantile(maxS[1], 1-qnt))
        cptSQ = (np.nanquantile(cpt, qnt))
        derSQ = (np.nanquantile(der, qnt))
        #######################################################################
        # Update in Dataframes
        #######################################################################
        xpid = monet.getXpId(fPath, xpidIx)
        updates = [
            xpid+i for i in (
                    ttiSQ, ttoSQ, wopSQ, rapSQ, 
                    list(mniSQ)+list(mnxSQ), list(poe), [cptSQ], [derSQ]
                )
        ]
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
                    {'POE': poe}, {'CPT': cpt}, {'DER': der}
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

