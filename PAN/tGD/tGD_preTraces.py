#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
import tGD_gene as drv
import tGD_plots as plot
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
# import warnings
# warnings.filterwarnings("ignore")


(USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (USR, DRV, AOI) = ('srv2', 'tGD', 'HLT')
(FMT, SKP, MF, FZ) = ('bz2', False, (True, True), False)
EXP = aux.EXPS
##############################################################################
# Setting up paths and style
##############################################################################
exp = EXP[0]
for exp in EXP:
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, DRV, exp
    )
    PT_IMG = PT_IMG + 'preTraces/'
    monet.makeFolder(PT_IMG)
    drive = drv.driveSelector(DRV, AOI)
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    # print(YRAN)
    STYLE = {
        "width": .5, "alpha": .9, "dpi": 200, "legend": True,
        "aspect": .5, "colors": CLR, "xRange": [0, (365*5)],
        "yRange": YRAN # (0, 7.5e3)
    }
    # if (AOI=='TRS') or (AOI=='WLD'):
    #     STYLE['yRange'] = (STYLE['yRange'][0], STYLE['yRange'][1]*2)
    # elif (AOI=='ECO'):
    #     STYLE['yRange'] = (STYLE['yRange'][0], STYLE['yRange'][1]*4)
    # else: 
    #     STYLE['yRange'] = (STYLE['yRange'][0], STYLE['yRange'][1])
    STYLE['aspect'] = monet.scaleAspect(1/3, STYLE)
    tS = datetime.now()
    aux.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'PreTraces '+AOI)
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    tyTag = ('sum', 'srp')
    if FZ:
        fLists = list(zip(*[fun.getFilteredFiles(
            PT_PRE+'*_00_*'+AOI+'*'+tp+'*',
            PT_PRE+'*'+AOI+'*'+tp+'*') for tp in tyTag]
        ))
    else:
        fLists = list(zip(
            *[sorted(glob(PT_PRE+'*'+AOI+'*'+tp+'*')) for tp in tyTag]
        ))
    ###########################################################################
    # Process files
    ###########################################################################
    (xpNum, digs) = monet.lenAndDigits(fLists)
    msg = '* Analyzing ({}/{})'
    for i in range(0, xpNum):
        print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
        (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
        name = fLists[i][0].split('/')[-1].split('.')[0][:-4]
        # Export plots --------------------------------------------------------
        plot.exportTracesPlot(
            repDta, name, STYLE, PT_IMG, append='TRA', 
            wopPrint=False, transparent=True
        )
    cl = [i[:-2]+'cc' for i in CLR]
    monet.exportGeneLegend(
            drive.get('gDict')['genotypes'], cl, PT_IMG+'/plt_{}.png'.format(AOI), 500
        )
    tE = datetime.now()
    print('* Analyzed ({}/{})                    '.format(xpNum, xpNum), end='\n')
