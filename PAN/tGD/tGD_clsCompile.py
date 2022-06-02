
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
    (USR, DRV, AOI, QNT, MTR) = ('srv', 'linkedDrive', 'WLD', '50', 'WOP')
else:
    (USR, DRV, AOI, QNT, MTR) = sys.argv[1:]
EXPS = aux.EXPS
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
exp = EXPS[0]
# for exp in EXPS:
###########################################################################
# Paths
###########################################################################
(header, xpidIx) = list(zip(*aux.DATA_HEAD))
###########################################################################
# Load landscape and drive
###########################################################################
(drive, land) = (drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE), [[0], ])
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, exp, 'SUMMARY')
# Time and head -----------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_MTR, tS, 
    '{} ClsCompile [{}:{}:{}:{}]'.format(DRV, DRV, QNT, AOI, MTR)
)
###########################################################################
# Flatten CSVs
###########################################################################
fName = sorted(glob('{}/*{}*{}*qnt.csv'.format(PT_SUMS, AOI, MTR)))
dfList = [pd.read_csv(i, sep=',') for i in fName]
dfMerged = pd.concat(dfList)
# Sorting columns ---------------------------------------------------------
outLabels = [x for x in list(dfMerged.columns) if len(x.split('_')) <= 1]
inLabels = [i[0] for i in aux.DATA_HEAD]
dfMerged.to_csv(
    path.join(PT_OUT, 'RAW_'+path.split(fName[0])[-1]), 
    index=False
)
# Scaling -----------------------------------------------------------------
for keyLabel in inLabels:
    dfMerged[keyLabel] = (dfMerged[keyLabel]/aux.DATA_SCA[keyLabel])
typesDict = {k: aux.DATA_TYPE[k] for k in dfMerged.columns if k[0]=='i'}
dfMerged = dfMerged.astype(typesDict)
dfMerged.to_csv(
    path.join(PT_OUT, 'SCA_'+path.split(fName[0])[-1]), 
    index=False
)
