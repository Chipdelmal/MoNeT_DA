#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd
import YDR_plots as plots
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, SET, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# (USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
(FMT, SKP, MF, FZ) = ('bz2', False, (True, True), False)
EXPS = ('000', '002', '004', '006', '008')
###############################################################################
# Setting up paths and style
###############################################################################
for EXP in EXPS:
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=11000),
        lnd.landSelector('SPA')
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, EXP
    )
    PT_IMG = PT_IMG + 'preTraces/'
    monet.makeFolder(PT_IMG)
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .25, "alpha": .15, "dpi": 250, "legend": True,
            "aspect": .25, "colors": CLR, "xRange": [0, (365*10)/3],
            "yRange": YRAN
        }
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    tS = datetime.now()
    aux.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'PreTraces')
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    tyTag = ('sum', 'srp')
    if FZ:
        fLists = list(zip(*[
                aux.getFilteredFiles(
                    PT_PRE+'*_00_*'+AOI+'*'+tp+'*',
                    PT_PRE+'*'+AOI+'*'+tp+'*'
                ) 
                for tp in tyTag
        ]))
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
        plots.exportTracesPlot(repDta, name, STYLE, PT_IMG, append='TRA')
        cl = [i[:-2]+'cc' for i in CLR]
    monet.exportGeneLegend(
            sumDta['genotypes'], cl, PT_IMG+'/plt_{}.png'.format(AOI), 500
        )
    tE = datetime.now()
    print('* Analyzed ({}/{})                   '.format(xpNum, xpNum), end='\n')
    print(monet.PAD)
