import sys
from os import path
from re import match
from glob import glob
from joblib import dump, load
from datetime import datetime
import numpy as np
from numpy.lib.arraypad import pad
import pandas as pd
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import seaborn as sns
from more_itertools import locate
from functools import reduce
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

if monet.isNotebook():
    (USR, LND, AOI, DRV, QNT) = ('dsk', 'PAN', 'HLT', 'LDR', '50')
else:
    (USR, LND, AOI, DRV, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
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
DATA = pd.read_csv(path.join(PT_OUT, fName_I))
# Features and labels ---------------------------------------------------------
COLS = list(DATA.columns)
(FEATS, LABLS) = (
    [i for i in COLS if i[0]=='i'], [i for i in COLS if i[0]!='i']
)
# Time and head --------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_OUT, tS,
    '{} DtaExplore [{}:{}:{}:{}]'.format(aux.XP_ID, aux.DRV, QNT, AOI, aux.THS)
)
###############################################################################
# Merge datasets on sex
###############################################################################
(sxML, sxNG, sxGV) = (
    DATA[DATA['i_sex']==1].drop(['i_sex', 'i_grp', 'i_mig'], axis=1), 
    DATA[DATA['i_sex']==2].drop(['i_sex', 'i_grp', 'i_mig'], axis=1), 
    DATA[DATA['i_sex']==3].drop(['i_sex', 'i_grp', 'i_mig'], axis=1)
)
mrgCol = [
    'i_ren', 'i_res', 'i_rsg', 'i_gsv', 'i_fch', 
    'i_fcb', 'i_fcr', 'i_hrm', 'i_hrf'
]
mrgDF = sxML.merge(
    sxNG, left_on=mrgCol, right_on=mrgCol, suffixes=['_ML', '_NG'], how='inner'
).merge(
    sxGV, left_on=mrgCol, right_on=mrgCol, suffixes=['_GV', '_GV'], how='inner'
).rename(columns={
    'TTI': 'TTI_GV', 'TTO': 'TTO_GV', 'WOP': 'WOP_GV',	
    'POE': 'POE_GV', 'POF': 'POF_GV', 'CPT': 'CPT_GV', 'MN': 'MN_GV'
})
###############################################################################
# Distributions
###############################################################################
(fig, ax) = plt.subplots(nrows=3, ncols=1)
sns.violinplot(x=mrgDF['CPT_ML'], ax=ax[0], size=.25, color='#03045e12', cut=0)
sns.stripplot(x=mrgDF['CPT_ML'], ax=ax[0], size=.25, color='#03045e32')
sns.stripplot(x=mrgDF['CPT_NG'], ax=ax[1], size=.25, color='#ff006e32')
sns.stripplot(x=mrgDF['CPT_GV'], ax=ax[2], size=.25, color='#3a86ff32')
for a in ax:
    a.set_xlim(0, 1)
plt.show()
fig.savefig(path.join(PT_IMG, 'SEX_DISTR.png'), dpi=500)
###############################################################################
# Compare Datasets
###############################################################################
(fig, ax) = plt.subplots(nrows=2, ncols=1)
sns.stripplot(x=mrgDF['CPT_ML']-mrgDF['CPT_NG'], ax=ax[0], size=.25, color='#ff006e32')
sns.stripplot(x=mrgDF['CPT_ML']-mrgDF['CPT_GV'], ax=ax[1], size=.25, color='#3a86ff32')
for a in ax:
    a.set_xlim(-.5, .5)
plt.show()
fig.savefig(path.join(PT_IMG, 'SEX_COMP.png'), dpi=500)