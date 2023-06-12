#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from os import path
import pandas as pd
from glob import glob
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
from more_itertools import locate
import GOP_aux as aux
import GOP_gene as drv
import GOP_gene_EPI as epi

plt.rcParams.update({
    "figure.facecolor":  (0.0, 0.0, 0.0, 0.0),
    "axes.facecolor":    (0.0, 0.0, 0.0, 0.0),
    "savefig.facecolor": (0.0, 0.0, 0.0, 0.0),
})

if monet.isNotebook():
    (USR, LND, DRV, AOI, SPE, QNT) = ('dsk', 'UpperRiver', 'HUM', 'CSS0', 'None', '50')
else:
    (USR, LND, DRV, AOI, SPE, QNT) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CLASSES_NUM = 5
WSIZE = 1
ASPECT = 1/10
LABELS = False
TO = 0 # aux.REL_START
###############################################################################
# Processing loop
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, LND, DRV, SPE
)
(ren, res) = (
    aux.getExperimentsIDSets(PT_PRE, skip=-1)[1],
    aux.getExperimentsIDSets(PT_PRE, skip=-1)[4]
)
rsIx = 0
for rsIx in range(len(res)-1):
    (i, rnIt) = (0, 10)
    for (i, rnIt) in enumerate(ren):
        (bSeries, tSeries, xSeries) = ([], [], [])
        strat = 1
        for strat in range(CLASSES_NUM):
            AOI = AOI[:3]+str(strat)
            (NH, NM) = aux.getPops(LND)
            (drive, land) = (
                drv.driveSelector(DRV, AOI, popSize=NM, humSize=NH),
                aux.landSelector()
            )
            (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
            (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
                USR, LND, DRV, SPE
            )
            # Time and head -----------------------------------------------------------
            if strat==0:
                tS = datetime.now()
                monet.printExperimentHead(
                    PT_PRE, PT_MTR, tS, 'EpiNumbers [{}:{}:{}]'.format(aux.XP_ID, fldr, AOI[:3])
                )
            ###########################################################################
            # Base experiments
            #   These are the experiments without any releases (for fractions)
            ###########################################################################
            # Get releases number set -------------------------------------------------
            (xpNum, digs) = monet.lenAndDigits(ren)
            # (i, rnIt) = (1, '20')
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
            if len(expIter)>1:
                exp = expIter[rsIx]
            else:
                exp = expIter[0]
            # Load base, mean and trace -----------------------------------------------
            (base, mean, trace) = [pkl.load(i) for i in exp[1:]]
            humanScaler = (NH*aux.AGE_DISTR_N[int(AOI[-1])])
            # Calculate base case -----------------------------------------------------
            baseCase = base['population'][TO:,0]
            baseCaseHuman = baseCase*humanScaler
            aggBases = aux.windowAggregate(baseCaseHuman, window=WSIZE, aggFun=sum)
            # Calculate treatment case ------------------------------------------------
            traceT = [tr[TO:, 0] for tr in trace['landscapes']]
            traceHuman = np.array([i*humanScaler for i in traceT])
            traceHumanQNT = np.quantile(traceHuman, int(QNT)/100, axis=0)
            # Calculate cases difference  ---------------------------------------------
            traceDiff = [(base['population']-tr)[TO:, 0] for tr in trace['landscapes']]
            traceDiffHuman = np.array([i*humanScaler for i in traceDiff])
            traceDiffHumanQNT = np.quantile(traceDiffHuman, int(QNT)/100, axis=0)
            # Quantiles ---------------------------------------------------------------
            qnt = np.quantile([sum(i) for i in traceHuman], int(QNT)/100)
            aggTraceCases = aux.windowAggregate(traceHumanQNT, window=WSIZE, aggFun=sum)
            qnt = np.quantile([sum(i) for i in traceDiffHuman], int(QNT)/100)
            aggCases = aux.windowAggregate(traceDiffHumanQNT, window=WSIZE, aggFun=sum)
            # Appends and Prints  -----------------------------------------------------
            bSeries.append(aggBases)
            tSeries.append(aggCases)
            xSeries.append(aggTraceCases)
        ###############################################################################
        # Export Files to Disk
        ###############################################################################
        expName = '{}-{}'.format(exp[2].split('/')[-1].split('-')[0], AOI[:3])
        print(expName)
        # Base case -------------------------------------------------------------------
        dfNoTreatment = pd.DataFrame(np.asarray(bSeries).T, columns=epi.AGE_GROUP_LABEL)
        dfNoTreatment.to_excel(path.join(PT_MTR, expName+'-base.xls'))
        dfNoTreatment.to_csv(path.join(PT_MTR, expName+'-base.csv'))
        # Treatment case --------------------------------------------------------------
        dfXTreatment = pd.DataFrame(np.asarray(xSeries).T, columns=epi.AGE_GROUP_LABEL)
        dfXTreatment.to_excel(path.join(PT_MTR, expName+'-treat.xls'))
        dfXTreatment.to_csv(path.join(PT_MTR, expName+'-treat.csv'))
        # Treatment difference --------------------------------------------------------
        dfTreatment = pd.DataFrame(np.asarray(tSeries).T, columns=epi.AGE_GROUP_LABEL)
        dfTreatment.to_excel(path.join(PT_MTR, expName+'-diff.xls'))
        dfTreatment.to_csv(path.join(PT_MTR, expName+'-diff.csv'))
        ###############################################################################
        # Plot
        ###############################################################################
        label = ('cases' if AOI[:3]=='CSS' else 'deaths')
        yran = (50*WSIZE if AOI[:3]=='CSS' else 1*WSIZE)
        tDelta = (50*WSIZE/5 if AOI[:3]=='CSS' else 1*WSIZE/5)
        colors = ['#ff006e', '#8338ec', '#3a86ff', '#f15bb5', '#04e762', '#3d348b']
        # Generate difference figure --------------------------------------------------
        (fig, ax) = plt.subplots(figsize=(8, 4))
        for ix in range(dfTreatment.shape[1]):
            ax.plot(dfTreatment.iloc[:,ix], color=colors[ix], lw=1)
        if LABELS:
            ax.legend(epi.AGE_GROUP_LABEL, bbox_to_anchor=(1, 1), frameon=False, loc="upper left")
            ax.set_xticks(np.arange(0, dfTreatment.shape[0], (30*5)/WSIZE))
            ax.set_yticks(np.arange(0, yran, tDelta))
            ax.set_title(LND)
            ax.grid(color='#00000055', linestyle='-', linewidth=.1)
            ax.set_xlabel("{}-day intervals".format(WSIZE))
            ax.set_ylabel("Aggregate difference in number of {}".format(label))
        else:
            ax.set_xticks([])
            ax.set_yticks([])
        ax.patch.set_facecolor('#00000000')
        ax.set_aspect(ASPECT * ((dfTreatment.shape[0]-1)/yran))
        ax.set_xlim(0, dfTreatment.shape[0]-1)
        ax.set_ylim(0, yran)
        fig.savefig(
            path.join(PT_MTR, expName+'-diff.png'), 
            dpi=500, pad_inches=0.025, bbox_inches="tight",
            transparent=True
        )
        plt.close(fig)
        # Generate base figure --------------------------------------------------------
        (fig, ax) = plt.subplots(figsize=(8, 4))
        for ix in range(dfNoTreatment.shape[1]):
            ax.plot(dfNoTreatment.iloc[:,ix], color=colors[ix], lw=1)
        if LABELS:
            ax.legend(epi.AGE_GROUP_LABEL, bbox_to_anchor=(1, 1), frameon=False, loc="upper left")
            ax.set_xticks(np.arange(0, dfTreatment.shape[0], (30*5)/WSIZE))
            ax.set_yticks(np.arange(0, yran, tDelta))
            ax.set_title(LND)
            ax.grid(color='#00000055', linestyle='-', linewidth=.1)
            ax.set_xlabel("{}-day intervals".format(WSIZE))
            ax.set_ylabel("Aggregate difference in number of {}".format(label))
        else:
            ax.set_xticks([])
            ax.set_yticks([])
        ax.set_aspect(ASPECT * ((dfTreatment.shape[0]-1)/yran))
        ax.set_xlim(0, dfTreatment.shape[0]-1)
        ax.set_ylim(0, yran)
        fig.savefig(
            path.join(PT_MTR, expName+'-base.png'), 
            dpi=500, pad_inches=0.025, bbox_inches="tight",
            transparent=True, facecolor=None
        )
        plt.close(fig)
        # Generate treat figure -------------------------------------------------------
        (fig, ax) = plt.subplots(figsize=(8, 4))
        for ix in range(dfXTreatment.shape[1]):
            ax.plot(dfXTreatment.iloc[:,ix], color=colors[ix], lw=1)
        if LABELS:
            ax.legend(epi.AGE_GROUP_LABEL, bbox_to_anchor=(1, 1), frameon=False, loc="upper left")
            ax.set_xticks(np.arange(0, dfTreatment.shape[0], (30*5)/WSIZE))
            ax.set_yticks(np.arange(0, yran, tDelta))
            ax.set_title(LND)
            ax.grid(color='#00000055', linestyle='-', linewidth=.1)
            ax.set_xlabel("{}-day intervals".format(WSIZE))
            ax.set_ylabel("Aggregate difference in number of {}".format(label))
        else:
            ax.set_xticks([])
            ax.set_yticks([])
        ax.set_aspect(ASPECT * ((dfTreatment.shape[0]-1)/yran))
        ax.set_xlim(0, dfTreatment.shape[0]-1)
        ax.set_ylim(0, yran)
        fig.savefig(
            path.join(PT_MTR, expName+'-treat.png'), 
            dpi=500, pad_inches=0.025, bbox_inches="tight",
            transparent=True, facecolor=None
        )
        # plt.close(fig)