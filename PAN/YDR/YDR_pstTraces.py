#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from glob import glob
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd


if monet.isNotebook():
    (USR, SET, DRV, AOI, QNT, THS) = (
        'dsk', 'homing', 'ASD', 'HLT', '50', '0.5'
    )
else:
    (USR, SET, DRV, AOI, QNT, THS) = (
        sys.argv[1], sys.argv[2], sys.argv[3], 
        sys.argv[4], sys.argv[5], sys.argv[6]
    )
###############################################################################
(header, xpidIx) = list(zip(*aux.getSummaryHeader(SET)))
xpPat = aux.getXPPattern(SET)
###############################################################################
EXPS = aux.EXPS
exp = EXPS[0]
for exp in EXPS:
    ###########################################################################
    # Load landscape and drive
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE), 
        lnd.landSelector('SPA')
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    xpPat = aux.getXPPattern(SET)
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, exp
    )
    PT_IMG = PT_IMG + 'pstTraces/'
    monet.makeFolder(PT_IMG)
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_PRE, PT_OUT, tS, 'SDP PstTraces {} [{}]'.format(DRV, AOI)
    )
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .75, "alpha": .75, "dpi": 300, "legend": True,
            "aspect": .25, "colors": CLR, "xRange": aux.XRAN, "yRange": YRAN
        }
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    ###########################################################################
    # Load postprocessed files
    ###########################################################################
    ###########################################################################
    pstPat = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
    pstFiles = [pstPat.format(i) for i in aux.DATA_NAMES]
    (dfTTI, dfTTO, dfWOP, dfRAP, dfMNX, dfPOE, dfCPT, dfDER) = [
        pd.read_csv(i) for i in pstFiles
    ]
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    (fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
    if aux.FZ:
        fltrPattern = aux.patternForReleases(SET, '00', AOI, 'srp', ext='bz')
    repFiles = monet.getFilteredFiles(
        PT_PRE+fltrPattern, globPattern.format('srp')
    )
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    (fNum, digs) = monet.lenAndDigits(repFiles)
    fmtStr = '{}+ File: {}/{}'
    (i, repFile) = (0, repFiles[0])
    for (i, repFile) in enumerate(repFiles):
        padi = str(i+1).zfill(digs)
        print(fmtStr.format(monet.CBBL, padi, fNum, monet.CEND), end='\r')
        (repDta, xpid) = (
                pkl.load(repFile),
                monet.getXpId(repFile, xpidIx)
            )
        xpRow = [
            monet.filterDFWithID(i, xpid, max=len(xpidIx)) for i in (
                dfTTI, dfTTO, dfWOP, dfMNX, dfPOE, dfCPT
            )
        ]
        (tti, tto, wop) = [float(row[THS]) for row in xpRow[:3]]
        (mnf, mnd, poe, cpt) = (
            float(xpRow[3]['min']), float(xpRow[3]['minx']), 
            float(xpRow[4]['POE']), float(xpRow[5]['CPT'])
        )
        # Traces ------------------------------------------------------------------
        pop = repDta['landscapes'][0][aux.STABLE_T][-1]
        STYLE['yRange'] = (0,  pop+pop*.5)
        STYLE['aspect'] = monet.scaleAspect(1, STYLE)
        monet.exportTracesPlot(
            repDta, repFile.split('/')[-1][:-6]+str(QNT), STYLE, PT_IMG,
            vLines=[tti, tto, mnd], hLines=[mnf*pop], 
            wop=wop, wopPrint=True, 
            cpt=cpt, cptPrint=True,
            poe=poe, poePrint=True
        )