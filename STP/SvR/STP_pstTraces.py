#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from glob import glob
import STP_aux as aux
import STP_gene as drv
import STP_plots as plot
import STP_functions as fun
import STP_dataProcess as da
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


if monet.isNotebook():
    (USR, DRV, AOI, REL, LND) = ('dsk', 'LDR', 'HLT', 'mixed', 'PAN')
else:
    (USR, DRV, AOI, REL, LND) = (sys.argv[1], 'LDR', sys.argv[2], sys.argv[3], sys.argv[4])
(SKP, THS, QNT, OVW, FZ) = (False, '0.1', '50', True, True)
tStable = 90

(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
PT_IMG = PT_IMG + 'pstTraces/'
monet.makeFolder(PT_IMG)
drive = drv.driveSelector(DRV, AOI, popSize=10*10000)
gene = drive.get('gDict')
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": .5, "alpha": .15, "dpi": 250, "legend": True, "aspect": .25,
        "colors": CLR, "xRange": [0, 365 * 6], "yRange": YRAN
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
tS = datetime.now()
monet.printExperimentHead(PT_ROT, PT_PRE, tS, 'UCIMI PstTraces '+AOI)
###########################################################################
# Load postprocessed files
###########################################################################
pstPat = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
pstFiles = [
    pstPat.format(i) for i in ('TTI', 'TTO', 'WOP', 'MNX', 'RAP', 'POE', 'CPT')
]
(dfTTI, dfTTO, dfWOP, dfMNX, dfRAP, dfPOE, dfCPT) = [
    pd.read_csv(i) for i in pstFiles
]
###########################################################################
# Load preprocessed files lists
###########################################################################
(fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*srp*')
if FZ:
    fltrPattern = PT_PRE+'*_00_*'+AOI+'*srp*'
repFiles = monet.getFilteredFiles(fltrPattern, globPattern)
repFiles.reverse()
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
            fun.getXpId(repFile, (1, 2, 3, 4, 5, 7))
        )
    xpRow = [
        da.filterDFWithID(i, xpid) for i in (
            dfTTI, dfTTO, dfWOP, dfMNX, dfPOE, dfCPT
        )
    ]
    (tti, tto, wop) = [float(row[THS]) for row in xpRow[:3]]
    (mnf, mnd, poe, cpt) = (
        float(xpRow[3]['min']), float(xpRow[3]['minx']), 
        float(xpRow[4]['POE']), float(xpRow[5]['CPT'])
    )
    # Traces ------------------------------------------------------------------
    if LND == 'PAN':
        tStable=0
    pop = repDta['landscapes'][0][tStable][-1]
    STYLE['yRange'] = (0,  pop+pop*.5)
    if AOI == 'ECO':
        STYLE['yRange'] = (STYLE['yRange'][0], STYLE['yRange'][1]*2)
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    plot.exportTracesPlot(
        repDta, repFile.split('/')[-1][:-6]+str(QNT), STYLE, PT_IMG,
        vLines=[tti, tto, mnd], hLines=[mnf*pop], 
        wop=wop, wopPrint=True, 
        cpt=cpt, cptPrint=True,
        poe=poe, poePrint=True
    )
