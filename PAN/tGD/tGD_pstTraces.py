#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import pandas as pd
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
import tGD_gene as drv
import tGD_plots as plot
import tGD_dataProcess as da
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import warnings
warnings.filterwarnings("ignore")

(USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (USR, DRV, AOI) = ('srv1', 'tGD', 'TRS')
(THS, QNT, OVW, FZ) = (0.75, '50', True, True)
EXPS = aux.EXPS
exp = EXPS[0]
for exp in EXPS:
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
    PT_IMG = PT_IMG + 'pstTraces/'
    monet.makeFolder(PT_IMG)
    drive = drv.driveSelector(DRV, AOI)
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
        "width": .5, "alpha": .9, "dpi": 200, "legend": True,
        "aspect": .5, "colors": CLR, "xRange": [0, (365*5)],
        "yRange": YRAN
    }
    STYLE['aspect'] = monet.scaleAspect(1/3, STYLE)
    tS = datetime.now()
    aux.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'PstTraces')
    ###########################################################################
    # Load postprocessed files
    ###########################################################################
    pstPat = PT_MTR+AOI+'_{}_'+QNT+'_qnt.csv'
    pstFiles = [pstPat.format(i) for i in ('TTI', 'TTO', 'WOP', 'MNX', 'RAP')]
    (dfTTI, dfTTO, dfWOP, dfMNX, _) = [pd.read_csv(i) for i in pstFiles]
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    repFiles = glob(PT_PRE+'*'+AOI+'*'+'srp'+'*')
    if FZ:
        fLists = fun.getFilteredFiles(
                PT_PRE+'*_00_*'+AOI+'*srp.bz',
                PT_PRE+'*'+AOI+'*'+'*srp.bz'
            )
    else:
        fLists = glob(PT_PRE+'*'+AOI+'*'+'*srp.bz')
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    msg = '* Plotting ({}/{})'
    filesNum = len(repFiles)
    for (i, repFile) in enumerate(repFiles):
        print(msg.format(i+1, filesNum), end='\r')
        (repDta, xpid) = (
            pkl.load(repFile),
            fun.getXpId(repFile, [1, 2, 3, 4, 5, 6, 7, 8])
        )
        xpRow = [da.filterDFWithID(i, xpid) for i in (dfTTI, dfTTO, dfWOP, dfMNX)]
        (tti, tto, wop) = [float(row[str(THS)]) for row in xpRow[:3]]
        (mnf, mnd) = (float(xpRow[3]['min']), float(xpRow[3]['minx']))
        pop = repDta['landscapes'][0][0][-1]
        plot.exportTracesPlot(
                repDta, repFile.split('/')[-1][:-6]+str(QNT), STYLE, PT_IMG,
                vLines=[tti, tto, mnd], hLines=[mnf*pop], wop=wop
            )
    monet.exportGeneLegend(
        repDta['genotypes'], [i[:-2]+'cc' for i in CLR],
        PT_IMG+'/plt_{}.png'.format(AOI), 500
    )
