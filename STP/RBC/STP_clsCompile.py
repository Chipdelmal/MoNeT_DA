

import sys
from glob import glob
from datetime import datetime
from os import path
from re import match
import numpy as np
import pandas as pd
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd


if monet.isNotebook():
    (USR, LND, AOI, QNT, MTR) = ('dsk', 'PAN', 'HLT', '90', 'CPT')
    JOB = aux.JOB_DSK
else:
    (USR, LND, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
    JOB = aux.JOB_SRV
EXPS = aux.getExps(LND)
###############################################################################
# Paths
###############################################################################
(drive, land) = (
    drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND)
)
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
###############################################################################
# Flatten CSVs
###############################################################################
fName = [glob('{}/*{}*{}*.csv'.format(i, AOI, MTR))[0] for i in PT_SUMS]
dfList = [pd.read_csv(i, sep=',') for i in fName]
for (df, exp) in zip(dfList, EXPS):
    df['i_mig'] = [int(exp)]*df.shape[0]
dfMerged = pd.concat(dfList)
# Sorting columns -------------------------------------------------------------
outLabels = [x for x in list(dfMerged.columns) if len(x.split('_')) <= 1]
inLabels = [i[0] for i in aux.DATA_HEAD]
inLabels.append('i_mig')
dfMerged = dfMerged.reindex(inLabels+outLabels, axis=1)
dfMerged.to_csv(
    path.join(PT_OUT, 'RAW_'+path.split(fName[0])[-1]), 
    index=False
)
# Scaling ---------------------------------------------------------------------
for keyLabel in inLabels:
    dfMerged[keyLabel] = (dfMerged[keyLabel]/aux.DATA_SCA[keyLabel])
dfMerged.to_csv(
    path.join(PT_OUT, 'SCA_'+path.split(fName[0])[-1]), 
    index=False
)
###############################################################################
# Load MLR dataset
###############################################################################
# i = PT_SUMS[0]
# fName = glob('{}/*{}*{}*.bz'.format(i, AOI, MTR))[0]
# probe = pkl.load(fName)
# keys = list(probe.keys())
# {tuple(j): probe[j]['CPT'] for j in keys}
# probe[keys[5]]