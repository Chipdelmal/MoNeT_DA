
import sys
from datetime import datetime
import numpy as np
from os import path
import pandas as pd
from re import match
import seaborn as sns
from scipy import stats
import MoNeT_MGDrivE as monet
import PYF_aux as aux
import matplotlib.pyplot as plt


if monet.isNotebook():
    (USR, LND, MTR, QNT) = ('dsk', 'PAN', 'WOP', '90')
else:
    (USR, LND, MTR, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

(ERR, OVW) = (False, True)
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
EXPS = ('male', 'gravidFemale', 'nonGravidFemale')
FEATS = ['i_pop', 'i_ren', 'i_res', 'i_mad', 'i_mat', 'i_grp']
SCA = 100000000
###############################################################################
# Setting up paths
###############################################################################
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR, PT_MOD) = aux.selectPath(
    USR, LND
)
PT_IMG = PT_IMG + 'pstModel/'
monet.makeFolder(PT_IMG)
tS = datetime.now()
monet.printExperimentHead(PT_DTA, PT_IMG, tS, 'PYF ClsPreprocess ')
###############################################################################
# Setup constants (user input)
###############################################################################
OPRAN = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 10))
(DTA_ITYPES, DTA_OTYPES) = (
    {
        'i_pop': 'int8', 'i_ren': 'int8', 'i_res': 'int8',
        'i_mad': 'int8', 'i_mat': 'int8'
    },
    'int8'
)
###############################################################################
# Read dataset and drop non-needed columns
###############################################################################
DTA_RAW = pd.read_csv(path.join(PT_MTR, ID_MTR))
# Get group 1 and drop the column from dataset (panmictic sim) ----------------
filterRules = (DTA_RAW['i_grp'] == 0, )
fltr = [all(i) for i in zip(*filterRules)]
DTA_RAW = DTA_RAW[fltr]
DTA_RAW = DTA_RAW.drop(['i_grp'], axis=1)
DTA_COLS = list(DTA_RAW.columns)
LBS = list(filter(lambda v: match('0.*', v), DTA_COLS))
# Clean dataset for modification ----------------------------------------------
DTA_CLN = DTA_RAW.copy()
###############################################################################
# Classify output
###############################################################################
for ths in LBS:
    grpMtr = np.asarray(DTA_CLN[ths])
    groupBools = [
        [i[0]*365 <= feat < i[1]*365 for i in OPRAN] for feat in grpMtr
    ]
    groupIx = [i.index(True) for i in groupBools]
    DTA_CLN[ths] = groupIx
###############################################################################
# Sort and coerce data output
###############################################################################
DTA_CLN = DTA_CLN.astype(DTA_ITYPES)
DTA_CLN = DTA_CLN.astype({i: DTA_OTYPES for i in LBS})
# Sort alphabetically --------------------------------------------------------
colsSorted = sorted(list(DTA_CLN.columns.values), reverse=True)
DTA_CLN = DTA_CLN[colsSorted]
###############################################################################
# Export
###############################################################################
DTA_CLN.to_csv(path.join(PT_MTR, 'CLN_'+ID_MTR), index=False)