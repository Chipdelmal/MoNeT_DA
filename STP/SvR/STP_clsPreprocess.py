

import sys
from datetime import datetime
from os import path
from re import match
import numpy as np
import pandas as pd
import MoNeT_MGDrivE as monet
from sklearn.preprocessing import LabelBinarizer

if monet.isNotebook():
    (MTR, QNT) = ('CPT', '50')
else:
    (MTR, QNT) = (sys.argv[1], sys.argv[2])
###############################################################################
# Setup constants (user input)
###############################################################################
if MTR == 'WOP':
    OPRAN = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 15))
elif MTR == 'TTI':
    OPRAN = ((0, .15), (.15, .25), (.25, .5), (.5, 3), (3, 15))
elif MTR == 'TTO':
    OPRAN = ((0, 2), (2, 4), (4, 6), (6, 9), (9, 15))
elif MTR == 'CPT':
    OPRAN = ((0, .2), (.2 , .4), (.4, .6), (.6, .8), (.8, 1))
# Sex categories --------------------------------------------------------------
SEX_CATS = {
    'male': (0, 'i_smx'), 
    'gravidFemale': (1, 'i_sgv'), 
    'nonGravidFemale': (2, 'i_sgn')
}
# Data types ------------------------------------------------------------------
(DTA_ITYPES, DTA_OTYPES) = (
    {
        'i_ren': 'int8', 'i_smx': np.bool_,
        'i_sgv': np.bool_, 'i_sgn': np.bool_,
        'i_qnt': 'int8'
    },
    'int8'
)
###############################################################################
# Create directories structure
###############################################################################
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
PT_ROT = '/home/chipdelmal/Documents/WorkSims/STP/PAN/'
(PT_IMG, PT_MOD, PT_OUT) = (
    PT_ROT + 'img/', PT_ROT + 'MODELS/', PT_ROT + 'SUMMARY/'
)
PT_DTA = '{}{}_{}'.format(PT_OUT, 'Full', ID_MTR)
[monet.makeFolder(i) for i in (PT_OUT, PT_MOD)]
tS = datetime.now()
monet.printExperimentHead(PT_DTA, PT_OUT, tS, 'UCIMI ML-Class Clean '+QNT)
###############################################################################
# Read dataset and drop non-needed columns
###############################################################################
DTA_RAW = pd.read_csv(PT_DTA)
DTA_RAW = DTA_RAW.drop(DTA_RAW.columns[0], axis=1)
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
# One-hot sex encoder
###############################################################################
sexEntries = DTA_RAW['i_sex']
sexCats = list(sexEntries.unique())
inSexCats = list(SEX_CATS.keys())
# Sanity check ----------------------------------------------------------------
if not (sexCats == inSexCats):
    print('Missmatch between defined and present sexes')
# Replace with numeric labels -------------------------------------------------
sexEntriesLbls = [SEX_CATS[i][0] for i in sexEntries]
DTA_CLN['i_sex'] = sexEntriesLbls
# One-hot encode sex ----------------------------------------------------------
sexOH = LabelBinarizer().fit_transform(DTA_CLN['i_sex']).T
for (i, cat) in enumerate(inSexCats):
    DTA_CLN[SEX_CATS[cat][1]] = sexOH[i]
# Drop the 'i_sex' label as it is redundant with one-hot ----------------------
DTA_CLN = DTA_CLN.drop(['i_sex'], axis=1)
# Add Quantile as Feature -----------------------------------------------------
DTA_CLN['i_qnt'] = [QNT] * DTA_CLN.shape[0]
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
DTA_CLN.to_csv(path.join(PT_OUT, 'CLN_'+ID_MTR), index=False)
