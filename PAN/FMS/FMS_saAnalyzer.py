
from os import sys
from os import path
import numpy as np
import pandas as pd
import compress_pickle as pkl
from SALib.sample import saltelli
import MoNeT_MGDrivE as monet
import FMS_aux as aux
import FMS_gene as drv


if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS) = ('srv', 'PGS', '50', 'HLT', '0.1')
else:
    (USR, DRV, QNT, AOI, THS) = sys.argv[1:]
###############################################################################
# Setting Paths Up and Reading SA Constants
###############################################################################
(SAMPLES_NUM, VARS_RANGES) = (aux.SA_SAMPLES, aux.SA_RANGES)
(drive, land) = (
    drv.driveSelector(DRV, 'HLT', popSize=aux.POP_SIZE), 
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, fldr)
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
###############################################################################
# Read SA Files
###############################################################################
(PROBLEM, SAMPLER, EXP) = (
    pkl.load(path.join(PT_MTR, 'SA_experiment.pkl')),
    np.load(path.join(PT_MTR, 'SA_experiment.npy')),
    pd.read_csv (path.join(PT_MTR, 'SA_experiment.csv'))
)
###############################################################################
# Read Results CSV
###############################################################################
thsStr = str(int(float(THS)*100))
(fName_I, fName_R, fName_C) = (
    'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'REG_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'CLS_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr)
)
RES = pd.read_csv(path.join(PT_OUT, fName_I))
###############################################################################
# Assemble Output Vector
###############################################################################
headExp = list(EXP.columns)
headRes = [i for i in RES.columns if i[0]=='i']
saVars = set([i[0] for i in ([i for i in VARS_RANGES if (len(i[1])>1)])])
saCnst = set([i[0] for i in ([i for i in VARS_RANGES if (len(i[1])<=1)])])
rsnst = set([i.split('_')[-1] for i in headRes]) - set(PROBLEM['names'])
# Generate filter -------------------------------------------------------------
ix = 0
rowVals = EXP.iloc[ix].to_dict()
# Fix discrepancy in release size
rowVals['res'] = rowVals['rer']
rowVals.pop('rer')
# Add group id to filter
rowVals['grp'] = 0
# Assemble the filter
fltr = {f'i_{k}': v for k, v in rowVals.items()}
# Filter Results for entry ----------------------------------------------------
ks = list(fltr.keys())
rowFilterMtx = [np.isclose(RES[k], fltr[k]) for k in ks]
boolFilter = [all(i) for i in zip(*rowFilterMtx)]

