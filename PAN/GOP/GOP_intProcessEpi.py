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
    '{} IntProcessEpi [{}:{}:{}]'.format(aux.XP_ID, fldr, LND, AOI)
)
###############################################################################
# Processing loop
###############################################################################
SCALER = 1000
# Average Response ------------------------------------------------------------
preFiles = glob(path.join(PT_PRE, '*{}*sum.bz'.format(AOI)))

ix = 0
pre = pkl.load(preFiles[ix])

# Incidence per 1000 instead of per capita ------------------------------------
preSca = pre['population']*NH
(totalPop, incPop) = (preSca[:,-1], preSca[:,0])
preSca[:,1] = totalPop-incPop*SCALER
preFix = {'genotypes': pre['genotypes'], 'population': preSca}
preFix


# Traces ----------------------------------------------------------------------
preFiles = glob(path.join(PT_PRE, '*{}*srp.bz'.format(AOI)))

ix = 1
pre = pkl.load(preFiles[ix])

SCALER = 1000
# Incidence per 1000 instead of per capita ------------------------------------
preSca = pre['landscapes']
pop = preSca[0]
for (ix, pop) in enumerate(preSca):
    pop = pop*NH
    (totalPop, incPop) = (pop[:,-1], pop[:,0])
    pop[:,1] = totalPop-incPop*SCALER
    preSca[ix] = pop
preFix = {'genotypes': pre['genotypes'], 'landscapes': preSca}

# import pandas as pd
# df = pd.read_csv(PT_DTA+'/ANALYZED/E_00_00000_0000000/H_Mean_0001.csv')
# (pixO, pixF) = [list(df.columns).index(i) for i in ('clin_inc00_01', 'clin_inc08_09')]
# df.iloc[:,pixO:pixF+1].sum(axis=1)