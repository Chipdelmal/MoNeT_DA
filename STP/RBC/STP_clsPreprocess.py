
import sys
from glob import glob
from datetime import datetime
from os import path
from re import match
import numpy as np
import pandas as pd
import compress_pickle as pkl
from sklearn.preprocessing import LabelBinarizer
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_auxDebug as dbg
import STP_gene as drv
import STP_land as lnd
import MoNeT_MGDrivE as monet
# https://machinelearningmastery.com/feature-selection-with-real-and-categorical-data/


if monet.isNotebook():
    (USR, LND, AOI, DRV, QNT) = ('srv', 'PAN', 'HLT', 'LDR', '50')
else:
    (USR, LND, AOI, DRV, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
EXPS = aux.getExps(LND)
###############################################################################
# Paths
###############################################################################
(fName_I, fName_R, fName_C) = (
    'A_SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, int(float(aux.THS)*100)),
    'REG_{}_{}Q_{}T.csv'.format(AOI, QNT, int(float(aux.THS)*100)),
    'CLS_{}_{}Q_{}T.csv'.format(AOI, QNT, int(float(aux.THS)*100)),
)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND, USR=USR)
)
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND, DRV)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
# Time and head --------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_OUT, tS, 
    '{} ClsPreProcess[{}:{}:{}]'.format(aux.XP_ID, DRV, QNT, AOI)
)
###############################################################################
# Load DF
###############################################################################
dfRaw = pd.read_csv(path.join(PT_OUT, fName_I))
###############################################################################
# One-Hot Sex
###############################################################################
oneHotSex = dbg.Binarizer().fit_transform(dfRaw.i_sex)
oneHotSexDF = pd.DataFrame(oneHotSex, columns=aux.SEX_CATS)
dfClean = pd.concat([oneHotSexDF, dfRaw.drop('i_sex', axis=1)], axis=1)
dfClean.to_csv(path.join(PT_OUT, fName_R), index=False)
###############################################################################
# Categorize outputs
###############################################################################
dfCat = dfClean.copy()
tCats = (
    aux.ML_CPT_CATS, aux.ML_POE_CATS, aux.ML_POF_CATS,
    aux.ML_WOP_CATS, aux.ML_TTI_CATS, aux.ML_TTO_CATS, 
    aux.ML_MNX_CATS
)
for (mtr, ran) in zip(('CPT', 'POE', 'POF', 'WOP', 'TTI', 'TTO', 'MNF'), tCats):
    print('{}- {}:{}'.format(monet.CBBL, mtr, ran, monet.CEND))
    dfCat[mtr] = pd.cut(
        dfClean[mtr], bins=ran, labels=list(range(len(ran)-1))
    )
###############################################################################
# Export output
###############################################################################
dfCat.to_csv(path.join(PT_OUT, fName_C), index=False)

