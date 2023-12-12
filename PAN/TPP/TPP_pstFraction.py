#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
from glob import glob
import TPP_aux as aux
import TPP_gene as drv
import numpy as np
import compress_pickle as pkl
from datetime import datetime
import MoNeT_MGDrivE as monet
from more_itertools import locate
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
# import warnings
# warnings.filterwarnings("ignore")

if monet.isNotebook():
    (USR, LND, EXP, DRV, AOI) = (
        'zelda', 'Kenya', 'highEIR', 'HUM', 'CSS'
    )
else:
    (USR, LND, EXP, DRV, AOI) = sys.argv[1:]
GRID_REF = False
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'zelda':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
(NH, NM) = aux.getPops(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=NM, humSize=0),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, EXP)
PT_IMG = path.join(PT_IMG, 'preTraces')
monet.makeFolder(PT_IMG)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_PRE, PT_OUT, tS, 'PstFraction [{}:{}:{}]'.format(aux.XP_ID, fldr, AOI)
)
###########################################################################
# Probe experiments
#   sum: Analyzed data aggregated into one node
#   srp: Garbage data aggregated into one node
###########################################################################
i=0
monet.printProgress(i+1, 1, 2)
# Repetitions data (Garbage) ------------------------------------------
tracePat = aux.patternForReleases(0, AOI, 'srp', pad=0)
traceFiles = sorted(glob(PT_PRE+tracePat))
# Mean data (Analyzed) ------------------------------------------------
meanPat = aux.patternForReleases(0, AOI, 'sum', pad=0)
meanFiles = sorted(glob(PT_PRE+meanPat))
expNum = len(meanFiles)
# Patch for static reference file -------------------------------------
baseFiles = expNum*[f'{PT_PRE}{aux.REF_FILE}-{AOI}_00_sum.bz']
baseFNum = len(baseFiles)
# Create experiments iterator list ------------------------------------
expIter = list(zip(
    list(range(expNum)), baseFiles, meanFiles, traceFiles
))
# Check for potential miss-matches in experiments folders -------------
(meanFNum, tracFNum) = (len(meanFiles), len(traceFiles))
if (meanFNum!=tracFNum) or (baseFNum!=meanFNum) or (baseFNum!=tracFNum):
    errorString = 'Unequal experiments folders lengths ({}/{}/{})'
    sys.exit(errorString.format(baseFNum, meanFNum, tracFNum)) 
# Filter existing if needed -------------------------------------------
if aux.OVW == False:
    expIDPreDone = set(monet.splitExpNames(PT_OUT, ext='npy'))
    expIDForProcessing = [i.split('/')[-1][:-14] for i in meanFiles]
    expsIxList = list(locate(
        [(i in expIDPreDone) for i in expIDForProcessing], 
        lambda x: x!=True
    ))
    expIter = [expIter[i] for i in expsIxList]
###########################################################################
# Process data
###########################################################################
Parallel(n_jobs=JOB)(
    delayed(monet.pstFractionParallel)(
        exIx, PT_OUT
    ) for exIx in expIter
)

# lnd = pkl.load(expIter[1000][1])['population'].T
# for i in range(len(lnd)):
#     plt.plot(lnd[i])
# plt.ylim(0, YRAN)
# plt.close()

# ix = 1000
# ref = pkl.load(expIter[ix][1])['population']
# pop = pkl.load(expIter[ix][-1])['landscapes'][0]

# monet.getPopRatio(ref, pop, 1)
# np.max(pkl.load(fLists[-1][0])['population'], axis=0)

# dta = np.load(
#     path.join(PT_OUT, 'E_00920_00811_00965_0000620_0008532-CSS_00_rto.npy')
# )
# np.min(dta[0])