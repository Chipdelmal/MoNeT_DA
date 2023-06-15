#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
import pandas as pd
from glob import glob
from joblib import dump
from datetime import datetime
import MoNeT_MGDrivE as monet
import SDP_aux as aux
import SDP_gene as drv
import SDP_land as lnd

if monet.isNotebook():
    (USR, DRV, AOI, QNT, THS, TRC) = (
        'zelda', 'PGS', 'HLT', '50', '0.1', 'HLT'
    )
else:
    (USR, DRV, AOI, QNT, THS, TRC) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###########################################################################
# Paths
###########################################################################
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
    PT_OUT = path.join(PT_ROT, 'ML')
    PT_IMG = path.join(PT_OUT, 'img')
    [monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
    PT_SUMS = path.join(PT_ROT, 'SUMMARY')
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_ROT, PT_SUMS, tS, 
        '{} DtaExplore [{}:{}:{}:{}]'.format('PGG', DRV, QNT, AOI, THS)
    )
    ###############################################################################
    # Read CSV
    ###############################################################################
    thsStr = str(int(float(THS)*100))
    (fName_I, fName_R) = (
        'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
        'REG_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr)
    )
    (DATA, DATA_FILE) = (
        pd.read_csv(path.join(PT_OUT, fName_I)),
        pd.read_csv(path.join(PT_OUT, fName_R))
    )
    # Features and labels ---------------------------------------------------------
    COLS = list(DATA.columns)
    (FEATS, LABLS) = (
        [i for i in COLS if i[0]=='i'], [i for i in COLS if i[0]!='i']
    )
    ###############################################################################
    # Filter Output with Constraints
    ###############################################################################
    (renRge, resRge) = ((0, 52), (0, 50))
    wopRge = (-10*365, 15*365)
    fltr = (
        renRge[0] <= DATA['i_ren'], DATA['i_ren'] <= renRge[1],
        resRge[0] <= DATA['i_res'], DATA['i_res'] <= resRge[1]
    )
    constrained = DATA[list(map(all, zip(*fltr)))]
    constrainedFiles = DATA_FILE[list(map(all, zip(*fltr)))]
    ###############################################################################
    # Export
    ###############################################################################
    print('{}* Found {}/{} matches (Check filter if needed!){}'.format(
        monet.CBBL, constrained.shape[0], DATA.shape[0], monet.CEND
    ))
    constrained.to_csv(path.join(PT_OUT, 'DTA_FLTR.csv'), index=False)
    constrainedFiles.to_csv(path.join(PT_OUT, 'DTA_FLTR_Files.csv'), index=False)
    ###############################################################################
    # Transform Entries
    ###############################################################################
    (SCA, PAD) = (aux.DATA_SCA, aux.DATA_PAD)
    catSorting = [i for i in list(DATA.columns) if i[0]=='i']
    outSorting = [i for i in list(DATA.columns) if i[0]!='i']
    zipper = {i: (int(SCA[i]), PAD[i]) for i in catSorting}
    # print(outSorting)
    # Transform to fnames ---------------------------------------------------------
    expsNum = constrained.shape[0]
    (expsIter, skipped, counter) = ([[], []], 0, 0)
    ix = 1
    skipped = 0
    for ix in range(expsNum):
        print(
            '{}* Processing: {}/{}{}'.format(monet.CBBL, ix+1, expsNum, monet.CEND), 
            end='\r'
        )
        # row = constrained.iloc[ix]
        row = constrainedFiles.iloc[ix]
        i=0
        ins = [str(int(row[i])).zfill(zipper[i][1]) for i in zipper]
        fname = aux.XP_PTRN.format(*ins[:-1], TRC, '00', 'srp', 'bz') 
        prePath = PT_PRE.split('/')
        fpath = path.join('/'.join(prePath), fname)
        fpath.split('/')[-1]
        if path.isfile(fpath):
            (tti, tto, wop, poe, _, cpt, mnf) = [row[i] for i in outSorting]
            expsIter.append([
                counter, fpath,
                tti, tto, wop, mnf, 0, poe, cpt
            ])
            counter = counter + 1
        else:
            print(fname)
            skipped = skipped + 1
    print(
        '{}* Skipped (no PRE): {}/{}{}'.format(
            monet.CBBL, skipped, expsNum, monet.CEND
        )
    )
    ###############################################################################
    # Export iter
    ###############################################################################
    dump(expsIter, path.join(PT_OUT, 'DTA_PST_{}.job'.format(AOI)))