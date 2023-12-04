#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from os import path
from datetime import datetime
import compress_pickle as pkl
from joblib import Parallel, delayed
from more_itertools import locate
import MoNeT_MGDrivE as monet
import TPP_aux as aux
import TPP_gene as drv
import warnings

warnings.filterwarnings("ignore")
if monet.isNotebook():
    (USR, LND, EXP, DRV, AOI) = (
        'zelda', 'Kenya', 'highEIR', 'LDR', 'ECO'
    )
else:
    (USR, LND, EXP, DRV, AOI) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'zelda':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
# (NH, NM) = aux.getPops(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=int(50e6*2.5), humSize=0),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, EXP)
PT_IMG = path.join(PT_IMG, 'preTraces')
monet.makeFolder(PT_IMG)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_PRE, PT_IMG, tS, 
    '{} PreTraces [{}:{}:{}]'.format(aux.XP_ID, fldr, LND, AOI)
)
###############################################################################
# Style 
###############################################################################
# if DRV != 'HUM':
#     (CLR, YRAN) = (drive.get('colors'), (NM*drive.get('yRange')))
# else:
#     if AOI[:3] == 'MRT':
#         (CLR, YRAN) = (drive.get('colors'), (0, 0.5e-5))
#     else:
#         (CLR, YRAN) = (drive.get('colors'), (0, 1e-2))
CLR = drive.get('colors')
YRAN = drive.get('yRange')
STYLE = {
    "width": 0.5, "alpha": .005, "dpi": 750, "aspect": 1/5, 
    "colors": CLR, "legend": True,
    "xRange": aux.XRAN, "yRange": (0, YRAN)
}
###############################################################################
# Load preprocessed files lists
###############################################################################
tyTag = ('sum', 'srp')
(fltrPattern, globPattern) = ('dummy', path.join(PT_PRE, '*'+AOI+'*'+'{}'+'*'))
if aux.FZ:
    fltrPattern = PT_PRE + aux.patternForReleases('00', AOI, '*')
fLists = monet.getFilteredTupledFiles(fltrPattern, globPattern, tyTag)
expNum = len(fLists)
# Arrange file tuples ---------------------------------------------------------
expIter = list(zip(list(range(expNum, 0, -1)), fLists))
expIter.reverse()
# Semi hard-coded ren (NEEDS FIX!) --------------------------------------------
i = 1000
rens = []
for i in range(len(fLists)):
    fPat = fLists[i][0].split('/')[-1].split('-')[0].split('_')
    renS = int(fPat[1])
    if renS > 0:
        ren = [aux.REL_START+i*7 for i in range(renS)]
    else:
        ren = [0]
    rens.append(ren)
###############################################################################
# Process files
###############################################################################
(xpNum, digs) = monet.lenAndDigits(fLists)
# exIx = expIter[100]
Parallel(n_jobs=JOB)(
    delayed(aux.exportPreTracesParallel)(
        exIx, STYLE, PT_IMG, 
        xpNum=xpNum, digs=digs, autoAspect=True,
        border=True, borderColor='#000000AA', borderWidth=1,
        sampRate=1, 
        # vLines=[0, 0, 50+8, 50+8, 50+8] + [
        #     aux.REL_START + 8 + i*int(exIx[1][0].split('/')[-1].split('_')[3]) + 
        #     int(exIx[1][0].split('/')[-1].split('_')[3]) 
        #     for i in 
        #     range(
        #         int(exIx[1][0].split('/')[-1].split('_')[1])
        #     )
        # ],
        # hLines=np.arange(0, YRAN[1], YRAN[1]/4)
    ) for exIx in expIter
)
# Export gene legend ----------------------------------------------------------
sumDta = pkl.load(fLists[-1][0])
monet.exportGeneLegend(
    sumDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
    PT_IMG+'/legend_{}.png'.format(AOI), 500
)


# import matplotlib.pyplot as plt
# lnd = pkl.load(fLists[-1][-1])['landscapes']
# for i in range(len(lnd)):
#     plt.plot(lnd[i])
    
# np.max(pkl.load(fLists[-1][0])['population'], axis=0)