

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
(fName_I, fName_O) = (
    'SCA_{}_{}_{}_qnt.csv'.format(AOI, MTR, QNT),
    'CLN_{}_{}_{}_qnt.csv'.format(AOI, MTR, QNT)
)
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
# Load DF
###############################################################################
dfRaw = pd.read_csv(path.join(PT_OUT, fName_I))
###############################################################################
# One-Hot Sex
###############################################################################
oneHotSex = LabelBinarizer().fit_transform(dfRaw.i_sex)
oneHotSexDF = pd.DataFrame(oneHotSex, columns=aux.SEX_CATS)
dfClean = pd.concat([oneHotSexDF, dfRaw.drop('i_sex', axis=1)], axis=1)
dfClean = dfClean.astype(aux.DATA_TYPE)
###############################################################################
# Categorize output
###############################################################################
dfCat = dfClean.copy()
dfCat[MTR] = pd.cut(
    dfClean[MTR],
    bins=aux.ML_FRC_CATS,
    labels=list(range(len(aux.ML_FRC_CATS)-1))
)
###############################################################################
# Export output
###############################################################################
dfCat.to_csv(path.join(PT_OUT, fName_O), index=False)