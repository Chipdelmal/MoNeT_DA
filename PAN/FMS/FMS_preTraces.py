#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
from datetime import datetime
import compress_pickle as pkl
from joblib import Parallel, delayed
from more_itertools import locate
import MoNeT_MGDrivE as monet
import FMS_aux as aux
import FMS_gene as drv
import warnings
warnings.filterwarnings("ignore")

if monet.isNotebook():
    (USR, DRV, AOI) = ('srv', 'FMS5', 'HLT')
else:
    (USR, DRV, AOI) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, fldr)
PT_IMG = path.join(PT_IMG, 'preTraces')
monet.makeFolder(PT_IMG)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_DTA, PT_PRE, tS, 'PreTraces [{}:{}:{}]'.format(aux.XP_ID, fldr, AOI)
)
###############################################################################
# Style 
###############################################################################
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
    "width": .1, "alpha": .1, "dpi": 750, "aspect": 1/6, 
    "colors": CLR, "legend": True,
    "xRange": aux.XRAN, "yRange": (0, YRAN[1]*1.5)
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
i = 20
rens = []
for i in range(len(fLists)):
    fPat = fLists[i][0].split('/')[-1].split('-')[0].split('_')
    ren = [50+i*7 for i in range(int(fPat[1]))]
    rens.append(ren)
###############################################################################
# Process files
###############################################################################
(xpNum, digs) = monet.lenAndDigits(fLists)
Parallel(n_jobs=JOB)(
    delayed(aux.exportPreTracesParallel)(
        exIx, STYLE, PT_IMG, 
        xpNum=xpNum, digs=digs, autoAspect=True,
        border=True, borderColor='#000000AA', borderWidth=1,
        sampRate=1, vLines=[0, 0] + ren, # aux.RELEASES
        hLines=[aux.POP_SIZE, aux.POP_SIZE/2]
    ) for (exIx, ren) in zip(expIter, rens)
)
# Export gene legend ----------------------------------------------------------
sumDta = pkl.load(fLists[-1][0])
monet.exportGeneLegend(
    sumDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
    PT_IMG+'/legend_{}.png'.format(AOI), 500
)

# dbg = pkl.load('/RAID5/marshallShare/fem_pgSIT/ifegenia_5/PREPROCESS/'+'E_0004_000160-ECO_00_sum.bz')