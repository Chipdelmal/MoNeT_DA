#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from glob import glob
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import SDP_aux as aux
import SDP_gene as drv
import SDP_land as lnd


if monet.isNotebook():
    (USR, DRV, AOI, QNT, THS) = ('dsk', 'CRS', 'HLT', '50', '0.1')
else:
    (USR, DRV, AOI, QNT, THS) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
###############################################################################
mtrs = ('TTI', 'TTO', 'WOP', 'MNX', 'RAP', 'POE', 'CPT')
EXPS = ('000', '001', '010')
(tStable, FZ, FLTR) = (
    0, True, 
    ['*', '*', '*', '00', '*', AOI, '*', '{}', 'bz']
)

exp = EXPS[0]
###############################################################################
# Load landscape and drive
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=25e3), lnd.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, fldr, exp
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
        "aspect": .25, "colors": CLR, "xRange": [0, (365*2.5)],
        "yRange": YRAN
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
###########################################################################
# Load postprocessed files
###########################################################################
###########################################################################
pstPat = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
pstFiles = [pstPat.format(i) for i in mtrs]
(dfTTI, dfTTO, dfWOP, dfMNX, dfRAP, dfPOE, dfCPT) = [
    pd.read_csv(i) for i in pstFiles
]
###########################################################################
# Load preprocessed files lists
###########################################################################
(fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
if FZ:
    fltrPattern = aux.XP_PTRN.format(*FLTR).format('srp')
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
            monet.getXpId(repFile, (1, 2, 3, 4, 5, 7))
        )
    xpRow = [
        monet.filterDFWithID(i, xpid) for i in (
            dfTTI, dfTTO, dfWOP, dfMNX, dfPOE, dfCPT
        )
    ]
    (tti, tto, wop) = [float(row[THS]) for row in xpRow[:3]]
    (mnf, mnd, poe, cpt) = (
        float(xpRow[3]['min']), float(xpRow[3]['minx']), 
        float(xpRow[4]['POE']), float(xpRow[5]['CPT'])
    )
    # Traces ------------------------------------------------------------------
    pop = repDta['landscapes'][0][tStable][-1]
    STYLE['yRange'] = (0,  pop+pop*.5)
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    monet.exportTracesPlot(
        repDta, repFile.split('/')[-1][:-6]+str(QNT), STYLE, PT_IMG,
        vLines=[tti, tto, mnd], hLines=[mnf*pop], 
        wop=wop, wopPrint=True, 
        cpt=cpt, cptPrint=True,
        poe=poe, poePrint=True
    )