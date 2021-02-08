
import sys
from datetime import datetime
import numpy as np
from os import path
import pandas as pd
import seaborn as sns
from scipy import stats
import MoNeT_MGDrivE as monet
import PYF_dataAnalysis as da
import matplotlib.pyplot as plt


if monet.isNotebook():
    (USR, LND, MTR, QNT) = ('WOP', '90')
else:
    (USR, LND, MTR, QNT) = (sys.argv[1], sys.argv[2])

(ERR, OVW) = (False, True)
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
EXPS = ('male', 'gravidFemale', 'nonGravidFemale')
FEATS = ['i_pop', 'i_ren', 'i_res', 'i_mad', 'i_mat', 'i_grp']
SCA = 100000000
###############################################################################
# Setting up paths
###############################################################################
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
SEX_CATS = {
    'male': (0, 'i_smx'), 
    'gravidFemale': (1, 'i_sgv'), 
    'nonGravidFemale': (2, 'i_sgn')
}
(DTA_ITYPES, DTA_OTYPES) = (
    {
        'i_ren': 'int8', 'i_smx': np.bool_,
        'i_sgv': np.bool_, 'i_sgn': np.bool_,
        'i_qnt': 'int8'
    },
    'int8'
)