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
    (USR, LND, AOI, DRV, QNT) = ('dsk', 'PAN', 'HLT', 'LDR', '50')
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
    drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND)
)
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND, DRV)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img', 'heat')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
###############################################################################
# Select surface variables
###############################################################################
(HD_IND, kSweep) = (
    ['i_ren', 'i_res'], 'i_sex'
)
(xSca, ySca) = ('linear', 'linear')
# Scalers and sampling --------------------------------------------------------
(scalers, HD_DEP, _, cmap) = aux.selectDepVars(MOI, AOI)
(ngdx, ngdy) = (1000, 1000)
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
if MOI == 'TTI':
    (zmin, zmax) = (45, 90)
else:
    (zmin, zmax) = (min(DATA[MOI]), max(DATA[MOI]))
# (zmin, zmax) = (-0.1, max(DATA[MOI]))
(lvls, mthd) = (np.arange(zmin*.9, zmax*1.1, (zmax-zmin)/20), 'linear')
# (lvls, mthd) = (np.arange(-0.1, 1.1, 1.5/20), 'nearest')
# Filter the dataframe --------------------------------------------------------
headerInd = [i for i in DATA.columns if i[0]=='i']
uqVal = {i: list(DATA[i].unique()) for i in headerInd}
# Add zeroes to dataframe -----------------------------------------------------
outFix = {
    'TTI': max(DATA['TTI']), 'TTO': max(DATA['TTO']), 'WOP': min(DATA['WOP']),
    'POE': min(DATA['POE']), 'POF': max(DATA['POF']), 'CPT': max(DATA['CPT']),
    'MNF': max(DATA['MNF'])
}
amend = uqVal.copy()
amend['i_res'] = [0]
amendFact = list(ParameterGrid(amend))
amendDict = [{**i, **outFix} for i in amendFact]
DATA = DATA.append(amendDict, ignore_index=True)
amend = uqVal.copy()
amend['i_ren'] = [0]
amendFact = list(ParameterGrid(amend))
amendDict = [{**i, **outFix} for i in amendFact]
DATA = DATA.append(amendDict, ignore_index=True)
###############################################################################
# Export amended dataset
###############################################################################
DATA.to_csv(path.join(PT_OUT, 'A_'+fName_I), index=False)