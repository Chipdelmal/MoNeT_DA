import sys
from math import exp
from os import path
from re import match
from glob import glob
from itertools import product
from joblib import dump, load
from datetime import datetime
import numpy as np
from numpy.lib.arraypad import pad
import pandas as pd
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
from more_itertools import locate
from sklearn.model_selection import ParameterGrid
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

if monet.isNotebook():
    (USR, LND, AOI, DRV, QNT) = ('lab', 'SPA', 'HLT', 'LDR', '50')
else:
    (USR, LND, AOI, DRV, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
EXPS = aux.getExps(LND)
###############################################################################
# Paths
###############################################################################
EXPS = aux.getExps(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND, USR=USR)
)
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND, DRV)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img', 'heat')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
###############################################################################
# Read CSV
###############################################################################
thsStr = str(int(float(aux.THS)*100))
(fName_I, fName_R, fName_C) = (
    'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'REG_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'CLS_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr)
)
DATA = pd.read_csv(path.join(PT_OUT, fName_I))
###############################################################################
# Fix dataframe
###############################################################################
headerInd = [i for i in DATA.columns if i[0]=='i']
headerInd.remove('i_ren')
headerInd.remove('i_res')
uqRows = DATA[headerInd].drop_duplicates()
# Select values for padding ---------------------------------------------------
outFix = {
    'TTI': max(DATA['TTI']), 'TTO': max(DATA['TTO']), 'WOP': min(DATA['WOP']),
    'POE': min(DATA['POE']), 'POF': max(DATA['POF']), 'CPT': max(DATA['CPT']),
    'MNF': max(DATA['MNF'])
}
# Replace row values ----------------------------------------------------------
for i, row in uqRows.iterrows():
    uqRows.at[i, 'i_ren'] = 0
    uqRows.at[i, 'i_res'] = 0
    for j in outFix:
        uqRows.at[i, j] = outFix[j]
DATA = DATA.append(uqRows, ignore_index=True)
###############################################################################
# Export amended dataset
###############################################################################
DATA.to_csv(path.join(PT_OUT, 'A_'+fName_I), index=False)
