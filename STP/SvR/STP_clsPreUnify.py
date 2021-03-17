
import sys
from datetime import datetime
import numpy as np
from os import path
import pandas as pd
import seaborn as sns
from scipy import stats
import MoNeT_MGDrivE as monet
import STP_dataAnalysis as da
import matplotlib.pyplot as plt


if monet.isNotebook():
    (MTR,  QNT) = ('CPT', '50')
else:
    (MTR, QNT) = (sys.argv[1], sys.argv[2])
(ERR, OVW) = (False, True)
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
EXPS = ('male', 'gravidFemale', 'nonGravidFemale')
FEATS = ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv', 'i_grp']
SCA = 100000000
###############################################################################
# Create directories structure
###############################################################################
PT_ROT = '/home/chipdelmal/Documents/WorkSims/STP/PAN/'
PT_DTA = ['{}{}/SUMMARY/{}'.format(PT_ROT, exp, ID_MTR) for exp in EXPS]
PT_OUT = PT_ROT + 'SUMMARY/'
PT_IMG = PT_ROT + 'img/'
monet.makeFolder(PT_OUT)
###############################################################################
# Read and clean datasets
###############################################################################
tS = datetime.now()
monet.printExperimentHead(PT_DTA, PT_OUT, tS, 'UCIMI ML-Class Unify '+QNT)
dfRC = {
    i[0]: da.rescaleDataset(pd.read_csv(i[1]), SCA) for i in zip(EXPS, PT_DTA)
}
HEADER = list(dfRC['male'].columns)
(LBLS, FEAT_LVLS) = (
    sorted(list(set(HEADER) - set(FEATS))),
    [set(dfRC['male'][i].unique()) for i in FEATS]
)
###############################################################################
# Unify Dataframe
###############################################################################
strFull = '{}{}_{}'.format(PT_OUT, 'Full', ID_MTR)
if (not path.isfile(strFull)) or (OVW):
    df = da.unifySexesDataframe(dfRC, EXPS, FEATS, LBLS)
    df.to_csv(strFull)
