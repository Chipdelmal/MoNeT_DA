
import sys
from glob import glob
from datetime import datetime
from os import path
from re import match
import numpy as np
import pandas as pd
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import tGD_aux as aux
import tGD_gene as drv


if monet.isNotebook():
    (USR, DRV, AOI, QNT, MTR) = ('srv', 'linkedDrive', 'HLT', '50', 'TTI')
else:
    (USR, DRV, AOI, QNT, MTR) = sys.argv[1:]
EXPS = aux.EXPS
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
exp = EXPS[0]
###########################################################################
# Paths
###########################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    [[0], ]
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_OUT = path.join(PT_ROT, 'ML')
PT_OUT_ML = PT_OUT.replace('/100', '')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
# Time and head -----------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_SUMS, tS, 
    '{} ClsCompileML [{}:{}]'.format(DRV, AOI, MTR)
)
###########################################################################
# Flatten CSVs (Scaled Naming)
###########################################################################
fName = sorted(glob('{}/{}_{}_MLR.csv'.format(PT_SUMS, AOI, MTR)))
dfList = [pd.read_csv(i, sep=',') for i in fName]
dfMerged = pd.concat(dfList)
# Sorting columns ---------------------------------------------------------
outLabels = [x for x in list(dfMerged.columns) if len(x.split('_')) <= 1]
inLabels = [i[0] for i in aux.DATA_HEAD]
dfMerged = dfMerged.reindex(inLabels+outLabels, axis=1)
# Scaling -----------------------------------------------------------------
for keyLabel in inLabels:
    dfMerged[keyLabel] = (dfMerged[keyLabel]/aux.DATA_SCA[keyLabel])
typesDict = {k: aux.DATA_TYPE[k] for k in dfMerged.columns if k[0]=='i'}
dfMerged = dfMerged.astype(typesDict)
dfMerged.to_csv(
    path.join(PT_OUT_ML, 'SCA_'+path.split(fName[0])[-1]), 
    index=False
)
###########################################################################
# Flatten CSVs (Regular Naming)
###########################################################################
# Regular Naming -----------------------------------------------------------------
fName = sorted(glob('{}/{}_{}_MLR.csv'.format(PT_SUMS, AOI, MTR)))
dfList = [pd.read_csv(i, sep=',') for i in fName]
dfMerged = pd.concat(dfList)
# Sorting columns ---------------------------------------------------------
outLabels = [x for x in list(dfMerged.columns) if len(x.split('_')) <= 1]
inLabels = [i[0] for i in aux.DATA_HEAD]
dfMerged = dfMerged.reindex(inLabels+outLabels, axis=1)
# Scaling -----------------------------------------------------------------
typesDict = {i:int for i in list(aux.DATA_TYPE.keys())}
dfMerged = dfMerged.astype(typesDict)
dfMerged.to_csv(
    path.join(PT_OUT_ML, 'REG_'+path.split(fName[0])[-1]), 
    index=False
)
###########################################################################
# Load MLR dataset
###########################################################################
# i = PT_SUMS[0]
# MTR = 'CPT'
# fName = glob('{}/*{}*{}*.bz'.format(i, AOI, MTR))[0]
# probe = pkl.load(fName)
# keys = list(probe.keys())
# data = []
# for j in keys:
#     data.extend([list(j)+[d] for d in probe[j]['CPT']])
