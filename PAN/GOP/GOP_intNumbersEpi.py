#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
from matplotlib.pyplot import axis
from glob import glob
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
from more_itertools import locate
import compress_pickle as pkl
import GOP_aux as aux
import GOP_gene as drv


if monet.isNotebook():
    (USR, LND, DRV, AOI, SPE) = ('dsk', 'Brikama', 'HUM', 'CSS', 'None')
else:
    (USR, LND, DRV, AOI, SPE) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
(NH, NM) = aux.getPops(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=NM, humSize=NH),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, LND, DRV, SPE
)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_DTA, PT_DTA, tS, 
    '{} IntNumbersEpi [{}:{}:{}]'.format(aux.XP_ID, fldr, LND, AOI)
)
###########################################################################
# Base experiments
#   These are the experiments without any releases (for fractions)
###########################################################################
# Get releases number set -------------------------------------------------
ren = aux.getExperimentsIDSets(PT_PRE, skip=-1)[1]


(xpNum, digs) = monet.lenAndDigits(ren)
(i, rnIt) = (1, '26')

# Get base experiments pattern --------------------------------------------
monet.printProgress(i+1, xpNum, digs)
# Repetitions data (Garbage) ------------------------------------------
tracePat = aux.patternForReleases(rnIt, AOI, 'srp', pad=aux.DATA_PAD['i_ren'])
traceFiles = sorted(glob(PT_PRE+tracePat))
# Mean data (Analyzed) ------------------------------------------------
meanPat = aux.patternForReleases(rnIt, AOI, 'sum', pad=aux.DATA_PAD['i_ren'])
meanFiles = sorted(glob(PT_PRE+meanPat))
expNum = len(meanFiles)
# Patch for static reference file -------------------------------------
baseFiles = [aux.replaceExpBase(f, aux.REF_FILE) for f in meanFiles]
baseFNum = len(baseFiles)
###############################################################################
# Processing loop
###############################################################################
SCALER = 1
# Average Response ------------------------------------------------------------
preFiles = glob(path.join(PT_PRE, '*{}*sum.bz'.format(AOI)))
for (ix, fName) in enumerate(preFiles):
    pre = pkl.load(fName)
    # Incidence per 1000 instead of per capita --------------------------------
    preSca = pre['population']*NH
    (totalPop, incPop) = (preSca[:,-1], preSca[:,0])
    preSca[:,1] = totalPop-incPop*SCALER
    preSca[:,0] = incPop*SCALER
    # Re-assemble and export --------------------------------------------------
    preFix = {'genotypes': pre['genotypes'], 'population': preSca}
    pkl.dump(preFix, fName)
    # print(fName)
# pkl.load(fName)
# Traces Response -------------------------------------------------------------
preFiles = glob(path.join(PT_PRE, '*{}*srp.bz'.format(AOI)))
for (ix, fName) in enumerate(preFiles):
    pre = pkl.load(fName)
    # Incidence per 1000 instead of per capita ------------------------------------
    preSca = pre['landscapes']
    for (ix, pop) in enumerate(preSca):
        pop = pop*NH
        (totalPop, incPop) = (pop[:,-1], pop[:,0])
        pop[:,1] = totalPop-incPop*SCALER
        pop[:,0] = incPop*SCALER
        preSca[ix] = pop
    # Re-assemble and export --------------------------------------------------
    preFix = {'genotypes': pre['genotypes'], 'landscapes': preSca}
    pkl.dump(preFix, fName)