#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import PYF_aux as aux
import PYF_gene as drv
import PYF_land as lnd
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import PYF_functions as fun

if monet.isNotebook():
    (USR, DRV, AOI, LND, QNT) = ('dsk', 'PGS', 'HLT', 'PAN', '75')
else:
    (USR, DRV, AOI, LND, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
###############################################################################
mlr = True
(thiS, thoS, thwS, tapS) = (
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [int((i+1)*365-1) for i in range(5)]
    )
###############################################################################
(header, xpidIx) = (
        ('i_pop', 'i_ren', 'i_res', 'i_mad', 'i_mat', 'i_grp'),
        (1, 2, 3, 4, 5, 7)
    )
outLabels = ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE')
###############################################################################
# Setting up paths
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR, PT_MOD) = aux.selectPath(
    USR, LND
)
tS = datetime.now()
monet.printExperimentHead(PT_DTA, PT_OUT, tS, 'PYF PstProcess '+AOI)
###############################################################################
# Load landscape and drive
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=11000),
    lnd.landSelector(LND, PT_ROT)
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
###############################################################################
# Setup schemes
###############################################################################
pth = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
DFOPths = [pth.format(z) for z in outLabels]
# Setup experiments IDs -------------------------------------------------------
uids = aux.getExperimentsIDSets(PT_OUT, skip=-1)
(rer, ren, res, mad, mat, aoi, grp) = uids[1:]
(xpDict, smryDicts) = ({}, ({}, {}, {}, {}, {}))
# Get experiment files --------------------------------------------------------
ptrn = aux.XP_PAT.format('*', '*', '*', '*', '*', AOI, '*', 'rto', 'npy')
fPaths = sorted(glob(PT_OUT+ptrn))
(fNum, digs) = monet.lenAndDigits(fPaths)
qnt = float(int(QNT)/100)
# Setup dataframes ------------------------------------------------------------
outDFs = fun.initDFsForDA(fPaths, header, thiS, thoS, thwS, tapS)
(ttiDF, ttoDF, wopDF, tapDF, rapDF, poeDF) = outDFs
###############################################################################
# Iterate through experiments
###############################################################################
fmtStr = '{}+ File: {}/{}'
# (i, fPath) = (0, fPaths[0])
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
            monet.calcTTI(repRto, thiS),
            monet.calcTTO(repRto, thoS),
            monet.calcWOP(repRto, thwS)
        )
    (minS, maxS, _, _) = monet.calcMinMax(repRto)
    rapS = monet.getRatioAtTime(repRto, tapS)
    poe = fun.calcPOE(repRto)
    #######################################################################
    # Calculate Quantiles
    #######################################################################
    ttiSQ = [np.nanquantile(tti, qnt) for tti in ttiS]
    ttoSQ = [np.nanquantile(tto, 1-qnt) for tto in ttoS]
    wopSQ = [np.nanquantile(wop, 1-qnt) for wop in wopS]
    rapSQ = [np.nanquantile(rap, qnt) for rap in rapS]
    mniSQ = (np.nanquantile(minS[0], qnt), np.nanquantile(minS[1], qnt))
    mnxSQ = (np.nanquantile(maxS[0], qnt), np.nanquantile(maxS[1], 1-qnt))
    #######################################################################
    # Update in Dataframes
    #######################################################################
    xpid = aux.getXpId(fPath, xpidIx)
    vals = (ttiSQ, ttoSQ, wopSQ, rapSQ, list(mniSQ)+list(mnxSQ), list(poe))
    updates = [xpid+i for i in vals]
    for df in zip(outDFs, updates):
        df[0].iloc[i] = df[1]
    #######################################################################
    # Update in Dictionaries
    #######################################################################
    if mlr:
        outDict = [
                {int(i[0]*100): i[1] for i in zip(thiS, ttiS)},
                {int(i[0]*100): i[1] for i in zip(thoS, ttoS)},
                {int(i[0]*100): i[1] for i in zip(thwS, wopS)},
                {int(i[0]*100): i[1] for i in zip(tapS, rapS)},
                {
                    'mnl': minS[0], 'mnd': minS[1],
                    'mxl': maxS[0], 'mxd': maxS[1]
                }
            ]
        for dct in zip(smryDicts, outDict):
            dct[0][tuple(xpid)] = dct[1]
###########################################################################
# Export Data
###########################################################################
for df in zip(outDFs, DFOPths):
    df[0].to_csv(df[1], index=False)
if mlr:
    for (i, dict) in enumerate(smryDicts):
        lbl = outLabels[i]
        pth = PT_MTR+AOI+'_'+lbl+'_'+QNT+'_mlr.bz'
        pkl.dump(dict, pth, compression='bz2')

