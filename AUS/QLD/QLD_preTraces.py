#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
from datetime import datetime

from matplotlib.pyplot import vlines
import QLD_aux as aux
import QLD_gene as drv
import QLD_land as lnd
import QLD_functions as fun
# import STP_auxDebug as dbg
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import compress_pickle as pkl


if monet.isNotebook():
    (USR, AOI, LND, EXP) = ('dsk', 'HLT', '02', 's2')
    JOB = aux.JOB_DSK
else:
    (USR, AOI, LND, EXP) = (
        sys.argv[1], sys.argv[2], 
        sys.argv[3],  sys.argv[4]
    )
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
EXPS = aux.getExps(LND)
exp = EXP
for exp in [exp, ]:
    ###########################################################################
    # Setting up paths
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
        lnd.landSelector(USR, LND)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, LND
    )
    PT_IMG = path.join(PT_IMG, 'preTraces')
    monet.makeFolder(PT_IMG)
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_PRE, PT_IMG, tS, 
        '{} PreTraces [{}:{}:{}]'.format(aux.XP_ID, aux.DRV, exp, AOI)
    )
    ###########################################################################
    # Style 
    ###########################################################################
    ranScaler = 1
    if LND=='10':
        xRange = aux.XRAN
        ranScaler = 4
    elif LND=='01':
        xRange = (365*2, 5*365)
        ranScaler = .75
        aspect = .15
    else:
        xRange = aux.XRAN
        aspect = .125
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange') / ranScaler))
    STYLE = {
            "width": .5, "alpha": 0, "dpi": 1500, "legend": True,
            "aspect": aspect, "colors": CLR, "xRange": xRange, "yRange": YRAN,
            "format": 'png', 'ls': '-'
        }
    tS = datetime.now()
    # VLines ------------------------------------------------------------------
    if exp=='s1':
        rel = [
            0, 0, 731, 738, 745, 752, 759, 766, 773, 780, 787, 794, 801, 808, 
            733, 740, 747, 754, 761, 768, 775, 782, 789, 796, 803, 810
        ]
        wop=False
    elif exp=='s2':
        rel = [
            731, 5*365, 
            1096, 1103, 1110, 1117, 1124, 1131, 1138, 1145, 1152, 1159, 1166, 
            1173, 1098, 1105, 1112, 1119, 1126, 1133, 1140, 1147, 1154, 1161, 
            1168, 1175
        ]
        wop = True
    elif exp=='s3':
        rel = [
            731, 5*365
        ]
        wop = True
    else:
        rel = [0, 0]
        wop = False
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    tyTag = ('sum', 'srp')
    (fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
    # if aux.FZ:
    #     fltrPattern = PT_PRE + aux.patternForReleases('00', AOI, '*')
    fLists = monet.getFilteredTupledFiles(fltrPattern, globPattern, tyTag)
    expNum = len(fLists)
    # Arrange file tuples -----------------------------------------------------
    expIter = list(zip(list(range(expNum, 0, -1)), fLists))
    expIter.reverse()
    # NEEDS OVW FITLERING!!!!!!!!!! -------------------------------------------
    ###########################################################################
    # Process files
    ###########################################################################
    (xpNum, digs) = monet.lenAndDigits(fLists)
    Parallel(n_jobs=JOB)(
        delayed(fun.exportPreTracesParallel)(
            exIx, STYLE, PT_IMG, 
            xpNum=xpNum, digs=digs, autoAspect=True, vLines=rel,
            border=True, borderColor='#8184a7AA', borderWidth=1,
            transparent=True, wop=wop
        ) for exIx in expIter
    )
    # Export gene legend ------------------------------------------------------
    sumDta = pkl.load(fLists[-1][0])
    monet.exportGeneLegend(
        sumDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
        PT_IMG+'/legend_{}.png'.format(AOI), 500
    )
