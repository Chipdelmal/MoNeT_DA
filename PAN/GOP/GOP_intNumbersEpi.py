#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from glob import glob
import numpy as np
import MoNeT_MGDrivE as monet
from matplotlib.pyplot import axis
from more_itertools import locate
import compress_pickle as pkl
import GOP_aux as aux
import GOP_gene as drv
import GOP_gene_EPI as epi


if monet.isNotebook():
    (USR, LND, DRV, AOI, SPE, QNT) = ('srv', 'UpperRiver', 'HUM', 'CSS0', 'None', '50')
else:
    (USR, LND, DRV, AOI, SPE, QNT) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
tSeries = []
for ix in range(6):
    AOI = AOI[:3]+str(ix)
    (NH, NM) = aux.getPops(LND)
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=NM, humSize=NH),
        aux.landSelector()
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, LND, DRV, SPE
    )
    ###########################################################################
    # Base experiments
    #   These are the experiments without any releases (for fractions)
    ###########################################################################
    # Get releases number set -------------------------------------------------
    ren = aux.getExperimentsIDSets(PT_PRE, skip=-1)[1]
    (xpNum, digs) = monet.lenAndDigits(ren)
    (i, rnIt) = (1, '26')
    # Get base experiments pattern -------------------------------------------
    monet.printProgress(i+1, xpNum, digs)
    # Repetitions data (Garbage) ---------------------------------------------
    tracePat = aux.patternForReleases(rnIt, AOI, 'srp', pad=aux.DATA_PAD['i_ren'])
    traceFiles = sorted(glob(PT_PRE+tracePat))
    # Mean data (Analyzed) ---------------------------------------------------
    meanPat = aux.patternForReleases(rnIt, AOI, 'sum', pad=aux.DATA_PAD['i_ren'])
    meanFiles = sorted(glob(PT_PRE+meanPat))
    expNum = len(meanFiles)
    # Patch for static reference file ----------------------------------------
    baseFiles = [aux.replaceExpBase(f, aux.REF_FILE) for f in meanFiles]
    baseFNum = len(baseFiles)
    # Get Baseline -----------------------------------------------------------
    baseFiles = [aux.replaceExpBase(f, aux.REF_FILE) for f in meanFiles]
    baseFNum = len(baseFiles)
    # Check for potential miss-matches in experiments folders ----------------
    (meanFNum, tracFNum) = (len(meanFiles), len(traceFiles))
    if (meanFNum!=tracFNum) or (baseFNum!=meanFNum) or (baseFNum!=tracFNum):
        errorString = 'Unequal experiments folders lengths ({}/{}/{})'
        sys.exit(errorString.format(baseFNum, meanFNum, tracFNum))
    # Create experiments iterator list ---------------------------------------
    expIter = list(zip(
        list(range(expNum)), baseFiles, meanFiles, traceFiles
    ))
    # Filter existing if needed ----------------------------------------------
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
    # Load base, mean and trace -----------------------------------------------
    ix = 0
    exp = expIter[ix]
    (base, mean, trace) = [pkl.load(i) for i in exp[1:]]
    humanScaler = (NH*aux.AGE_DISTR_N[int(AOI[-1])])
    # Calculate cases difference ----------------------------------------------
    traceDiff = [(base['population']-tr)[aux.REL_START:,0] for tr in trace['landscapes']]
    traceDiffHuman = np.array([i*humanScaler for i in traceDiff])
    traceDiffHumanQNT = np.quantile(traceDiffHuman, int(QNT)/100, axis=0)
    # Quantiles ---------------------------------------------------------------
    qnt = np.quantile([sum(i) for i in traceDiffHuman], int(QNT)/100)
    aggCases = aux.windowAggregate(traceDiffHumanQNT, window=30, aggFun=sum)
    # Appends and Prints  -----------------------------------------------------
    tSeries.append(aggCases)
    print(AOI+': '+str(qnt))
print('\n')

dfTreatment = pd.DataFrame(np.asarray(tSeries).T, columns=epi.AGE_GROUP_LABEL)


# fig = plt.figure()
# ax = fig.add_subplot(111)
# for i in traceDiffHuman:
#     plt.plot(i)
# ax.set_ylim(0, .1)