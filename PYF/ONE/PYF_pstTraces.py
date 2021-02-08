
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from glob import glob
import PYF_aux as aux
import PYF_gene as drv
import PYF_land as lnd
import PYF_plots as plot
import PYF_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl



if monet.isNotebook():
    (USR, DRV, AOI, LND, QNT, THS) = ('dsk', 'PGS', 'HLT', 'PAN', '75', '0.1')
else:
    (USR, DRV, AOI, LND, QNT, THS) = (
        sys.argv[1], sys.argv[2], sys.argv[3],
        sys.argv[4], sys.argv[5], sys.argv[6]
    )
###############################################################################
(SKP, OVW, FZ, tStable) = (False, True, True, int(30/2))
###############################################################################
# Setting up paths
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND)
PT_IMG = PT_IMG + 'pstTraces/'
monet.makeFolder(PT_IMG)
tS = datetime.now()
monet.printExperimentHead(PT_DTA, PT_IMG, tS, 'PYF PstTraces '+AOI)
###############################################################################
# Load landscape and drive
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=20*62),
    lnd.landSelector(LND, PT_ROT)
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
###############################################################################
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": .2, "alpha": .15, "dpi": 500, "legend": True, "aspect": .25,
        "colors": CLR, "xRange": [0, 365 * 2.5], "yRange": YRAN
    }
###########################################################################
# Load postprocessed files
###########################################################################
pstPat = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
pstFiles = [pstPat.format(i) for i in ('TTI', 'TTO', 'WOP', 'MNX', 'RAP')]
(dfTTI, dfTTO, dfWOP, dfMNX, _) = [pd.read_csv(i) for i in pstFiles]
###########################################################################
# Load preprocessed files lists
###########################################################################
(fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*srp*')
if FZ:
    fltrPattern = PT_PRE+'*_000_*'+AOI+'*srp*'
repFiles = monet.getFilteredFiles(fltrPattern, globPattern)
# print(repFiles)
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
            aux.getXpId(repFile, (1, 2, 3, 4, 5, 7))
        )
    xpRow = [monet.filterDFWithID(i, xpid) for i in (dfTTI, dfTTO, dfWOP, dfMNX)]
    (tti, tto, wop) = [float(row[THS]) for row in xpRow[:3]]
    (mnf, mnd) = (float(xpRow[3]['min']), float(xpRow[3]['minx']))
    # Traces ------------------------------------------------------------------
    pop = repDta['landscapes'][0][tStable][-1]
    STYLE['yRange'] = (0,  pop+pop*.2)
    STYLE['aspect'] = monet.scaleAspect(.25, STYLE)
    monet.exportTracesPlot(
            repDta, repFile.split('/')[-1][:-6]+str(QNT), STYLE, PT_IMG,
            vLines=[tti, tto, mnd], hLines=[mnf*pop], wop=wop
        )
