

import sys
from os import path
from re import match
from glob import glob
from joblib import dump, load
from datetime import datetime
import numpy as np
import pandas as pd
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
# Read CSV
###############################################################################
thsStr = str(int(float(aux.THS)*100))
(fName_I, fName_R, fName_C) = (
    'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'REG_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'CLS_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr)
)
DATA = pd.read_csv(path.join(PT_OUT, fName_R))
###############################################################################
# Read ML
###############################################################################
fNameModel = (
    # 'CLS_{}_{}Q_{}T_{}_RF.joblib'.format(AOI, QNT, thsStr, 'WOP'),
    'CLS_{}_{}Q_{}T_{}_RF.joblib'.format(AOI, QNT, thsStr, 'CPT'),
    'CLS_{}_{}Q_{}T_{}_RF.joblib'.format(AOI, QNT, thsStr, 'TTI')
)
mdls = [load(path.join(PT_OUT, i)) for i in fNameModel]
###############################################################################
# Filter Output with Constraints
###############################################################################
renLim = (1, 20)
cptLim = .5
(ttiLim, wopLim) = (120, 2*365)
# Filter and return dataframe -------------------------------------------------
fltr = [
    DATA['i_grp'] == 0,
    DATA['i_ren'] > renLim[0], DATA['i_ren'] <= renLim[1],
    DATA['i_gsv'] < 1,
    DATA['CPT'] < cptLim,
    DATA['WOP'] > wopLim,
    DATA['TTI'] < ttiLim
]
boolFilter = [all(i) for i in zip(*fltr)]
daFltrd = DATA[boolFilter]
###############################################################################
# Filter Output with Constraints
###############################################################################
feats = [i for i in list(daFltrd.columns) if i[0]=='i']
ranges = {i: sorted(daFltrd[i].unique()) for i in feats}
daFltrd

daFltrd[feats]