#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import pandas as pd
from os import path
from glob import glob
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg

if monet.isNotebook():
    (USR, AOI, LND, QNT, THS) = ('dsk', 'HLT', 'PAN', '50', '0.5')
    JOB = aux.JOB_DSK
else:
    (USR, AOI, LND, QNT, THS) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
    JOB = aux.JOB_SRV
(EXPS, DRV) = (aux.getExps(LND), 'LDR')
(header, xpidIx) = list(zip(*aux.DATA_HEAD))
###############################################################################
# Processing loop
###############################################################################
exp = EXPS[0]
for exp in EXPS:
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
    PT_IMG = PT_IMG + 'pstTraces/'
    monet.makeFolder(PT_IMG)
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_OUT, PT_IMG, tS, 
        aux.XP_ID+' PstTraces[{}:{}:{}]'.format(DRV, exp, AOI)
    )
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .5, "alpha": .5, "dpi": 300, "legend": True,
            "aspect": 1, "colors": CLR, "xRange": aux.XRAN, "yRange": YRAN
        }
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    (fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
    if aux.FZ:
        fltrPattern = aux.patternForReleases(
            aux.NO_REL_PAT, AOI, 'srp', ext='bz'
        )
    repFiles = monet.getFilteredFiles(
        PT_PRE+fltrPattern, globPattern.format('srp')
    )
    expsNum = len(repFiles)
    ###########################################################################
    # Check if tuples cache is present and generate if not
    ###########################################################################
    tpsName = 'pstExp_{}_{}q_{}t.pkl'.format(AOI, QNT, int(float(THS)*100))
    cacheExists = path.isfile(path.join(PT_MTR, tpsName))
    if (not cacheExists) or (aux.OVW):
        # Load postprocessed files --------------------------------------------
        pstPat = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
        pstFiles = [pstPat.format(i) for i in aux.DATA_NAMES]
        (dfTTI, dfTTO, dfWOP, _, dfMNX, dfPOE, dfCPT, _) = [
            pd.read_csv(i) for i in pstFiles
        ]
        allDF = (dfTTI, dfTTO, dfWOP, dfMNX, dfPOE, dfCPT)
        # Filtered tuples -----------------------------------------------------
        fmtStr = '{}* Generating file tuples por processing...{}'
        print(fmtStr.format(monet.CBBL, monet.CEND), end='\r')
        expsIter = [None]*expsNum
        for i in range(expsNum):
            repFile = repFiles[i]
            xpid = monet.getXpId(repFile, xpidIx)
            xpRow = [
                monet.filterDFWithID(j, xpid, max=len(xpidIx)) for j in allDF
            ]
            (tti, tto, wop) = [float(row[THS]) for row in xpRow[:3]]
            (mnf, mnd, poe, cpt) = (
                float(xpRow[3]['min']), float(xpRow[3]['minx']), 
                float(xpRow[4]['POE']), float(xpRow[5]['CPT'])
            )
            expsIter[i] = (i, repFile, tti, tto, wop, mnf, mnd, poe, cpt)
        pkl.dump(expsIter, path.join(PT_MTR, tpsName))
        sys.stdout.write("\033[K")
    else:
        expsIter = pkl.load(path.join(PT_MTR, tpsName))
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    (fNum, digs) = monet.lenAndDigits(repFiles)
    Parallel(n_jobs=JOB)(
        delayed(dbg.exportPstTracesParallel)(
            exIx, expsNum,
            aux.STABLE_T, THS, QNT, STYLE, PT_IMG, 
            digs=digs, border=True, autoAspect=True, labelPos=(.8, .2)
        ) for exIx in expsIter
    )
    # Export gene legend ------------------------------------------------------
    repDta = pkl.load(repFiles[-1])
    monet.exportGeneLegend(
        repDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
        PT_IMG+'/legend_{}.png'.format(AOI), 500
    )
