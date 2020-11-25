

import pandas as pd
import MoNeT_MGDrivE as monet
from sklearn.preprocessing import LabelBinarizer


###############################################################################
# Setup constants (user input)
###############################################################################
(MTR, OVW, QNT) = ('WOP', True, '50')
(FTS, LBS) = (
    ['i_sex', 'i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv', 'i_grp'],
    ['0.5', '0.25', '0.1']
)
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
PROTECTION_YEARS = {
    'None': (0, 1), 
    'Low':  (1, 2), 
    'Mid':  (2, 3), 
    'High': (3, 5), 
    'Full': (5, 10)
}
SEX_CATS = {
    'mixed': 0,
    'gravidFemale': 1,
    'nonGravidFemale': 2
}
###############################################################################
# Create directories structure
###############################################################################
PT_ROT = '/home/chipdelmal/Documents/WorkSims/STP/PAN/'
PT_OUT = PT_ROT + 'SUMMARY/'
PT_DTA = '{}{}_{}'.format(PT_OUT, 'Full', ID_MTR)
PT_IMG = PT_ROT + 'img/'
PT_MOD = PT_ROT + 'MODELS/'
[monet.makeFolder(i) for i in (PT_OUT, PT_MOD)]
###############################################################################
# Read dataset and drop non-needed columns
###############################################################################
DTA_RAW = pd.read_csv(PT_DTA)
DTA_RAW = DTA_RAW.drop(DTA_RAW.columns[0], axis=1)
# Get group 1 and drop the column from dataset (panmictic sim) ----------------
filterRules = (
    DTA_RAW['i_grp'] == 0,
)
fltr = [all(i) for i in zip(*filterRules)]
DTA_RAW = DTA_RAW[fltr]
DTA_RAW = DTA_RAW.drop(['i_grp'],axis=1)
DTA_COLS = list(DTA_RAW.columns)
# Clean dataset for modification ----------------------------------------------
DTA_CLN = DTA_RAW.copy()
###############################################################################
# One-hot sex encoder
###############################################################################
sexEntries = DTA_RAW['i_sex']
sexCats = list(sexEntries.unique())
# Sanity check ----------------------------------------------------------------
if not(sexCats == list(SEX_CATS.keys())):
    print('Missmatch between defined and present sexes')
# Replace with numeric labels -------------------------------------------------
sexEntriesLbls = [SEX_CATS[i] for i in sexEntries]
DTA_CLN['i_sex'] = sexEntriesLbls
# One-hot encode sex ----------------------------------------------------------
sexOH = LabelBinarizer().fit_transform(DTA_CLN['i_sex'])