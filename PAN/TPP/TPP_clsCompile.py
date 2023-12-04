
import sys
from os import path
import pandas as pd
from glob import glob
from datetime import datetime
import MoNeT_MGDrivE as monet
import TPP_aux as aux
import TPP_gene as drv

if monet.isNotebook():
    (USR, LND, EXP, DRV, AOI, QNT, MTR) = (
        'zelda', 'Kenya', 'highEIR', 'LDR', 'HLT', '50', 'POE'
    )
else:
    (USR, LND, EXP, DRV, AOI, QNT, MTR) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'zelda':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###########################################################################
# Paths
###########################################################################
(NH, NM) = aux.getPops(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=NM, humSize=0),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, EXP)
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
# Time and head -----------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_SUMS, tS, 
    '{} ClsCompile [{}:{}:{}]'.format(DRV, QNT, AOI, MTR)
)
###########################################################################
# Flatten CSVs (Scaled Naming)
###########################################################################
fName = sorted(glob('{}/{}_{}_{}_qnt.csv'.format(PT_SUMS, AOI, MTR, QNT)))
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
    path.join(PT_OUT, 'SCA_'+path.split(fName[0])[-1]), 
    index=False
)
###########################################################################
# Flatten CSVs (Regular Naming)
###########################################################################
# Regular Naming -----------------------------------------------------------------
fName = sorted(glob('{}/{}_{}_{}_qnt.csv'.format(PT_SUMS, AOI, MTR, QNT)))
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
    path.join(PT_OUT, 'REG_'+path.split(fName[0])[-1]), 
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
