import sys
import random
import math
import subprocess
from os import path
from re import match
from glob import glob
from joblib import dump, load
from datetime import datetime
import numpy as np
from numpy.lib.arraypad import pad
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn import preprocessing
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
from more_itertools import locate
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

if monet.isNotebook():
    (USR, LND, AOI, DRV, QNT) = ('lab', 'PAN', 'HLT', 'LDR', '50')
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
# Filter Output with Constraints
###############################################################################
# Design constraints ----------------------------------------------------------
(sexLim, renLim, resLim) = (1, 15, .5)
# Goals constraints -----------------------------------------------------------
cptLim = (0.25, 1)
poeLim = (-.1, 1)
ttiLim = (-1, 365/6)
ttoLim = (-1, 6*365)
wopLim = (0, 10*365)
mnfLim = (0, 1000)
# Filter and return dataframe -------------------------------------------------
constrained = DATA[
    (cptLim[0] <= DATA['CPT']) & (DATA['CPT'] <= cptLim[1]) &
    (wopLim[0] <= DATA['WOP']) & (DATA['WOP'] <= wopLim[1]) &
    (ttiLim[0] <= DATA['TTI']) & (DATA['TTI'] <= ttiLim[1]) &
    (ttoLim[0] <= DATA['TTO']) & (DATA['TTO'] <= ttoLim[1]) &
    (poeLim[0] <= DATA['POE']) & (DATA['POE'] <= poeLim[1]) &
    (mnfLim[0] <= DATA['MNF']) & (DATA['MNF'] <= mnfLim[1]) &
    (DATA['i_ren'] <= renLim)  &
    (DATA['i_res'] <= resLim)  &
    (1e-2  >= DATA['i_gsv']) &
    DATA['i_sex'] == 1
]
constrained.shape
# Export data -----------------------------------------------------------------
print('{}* Found {}/{} matches (FLTR){}'.format(
	monet.CBBL, constrained.shape[0], DATA.shape[0], monet.CEND
))
constrained.to_csv(path.join(PT_OUT, 'DTA_FLTR.csv'), index=False)
###############################################################################
# Filter Output with Constraints
###############################################################################
# Design constraints ----------------------------------------------------------
(sexLim, renLim, resLim) = (1, 50, 1.5)
# Goals constraints -----------------------------------------------------------
cptLim = (-0.1, 1.1)
poeLim = (-.1, 1)
ttiLim = (-1, 4*365)
ttoLim = (-1, 6*365)
wopLim = (0, 10*365)
mnfLim = (0, 1)
# Filter and return dataframe -------------------------------------------------
constrained = DATA[
    (DATA['i_sex'] == sexLim)           &
    np.isclose(DATA['i_fch'], 0.175)    &
    np.isclose(DATA['i_fcb'], 0.117)    &
    np.isclose(DATA['i_fcr'], 0)        &
    np.isclose(DATA['i_hrm'], 1.0)      &
    np.isclose(DATA['i_hrf'], 0.956)    &
    np.isclose(DATA['i_rsg'], 0.079)    &
    np.isclose(DATA['i_gsv'], 1.e-02)   &
    (0 <= DATA['i_ren'])    & (DATA['i_ren'] <= renLim)         &
    (0 <= DATA['i_res'])    & (DATA['i_res'] <= resLim)
]
# print(DATA['i_fcb'].unique())
constrained.shape
# Export data -----------------------------------------------------------------
print('{}* Found {}/{} matches (FLTR_BD){}'.format(
	monet.CBBL, constrained.shape[0], DATA.shape[0], monet.CEND
))
constrained.to_csv(path.join(PT_OUT, 'DTA_FLTR_BD.csv'), index=False)
###############################################################################
# Sex
###############################################################################
partB = DATA[(DATA['WOP'] < 750)  & (DATA['i_sex'] == 1)]
partA = DATA[(1250 < DATA['WOP']) & (DATA['i_sex'] == 2)]
# Find intersections ----------------------------------------------------------
drops = ['TTI', 'TTO', 'POE', 'WOP', 'POF', 'CPT', 'MNF', 'i_sex']
dfs = [i.drop(drops, axis=1) for i in (partA, partB)]
inter = pd.merge(*dfs, 'inner')
pA = inter.copy()
pA['i_sex'] = [1]*inter.shape[0]
pB = inter.copy()
pB['i_sex'] = [2]*inter.shape[0]
pC = inter.copy()
pC['i_sex'] = [3]*inter.shape[0]
# Find intersections in main dataset ------------------------------------------
pFull = pd.merge(pd.merge(pA, pB, 'outer'), pC, 'outer')
pInter = DATA.merge(pFull)
# Export dataset --------------------------------------------------------------
print('{}* Found {}/{} matches (FLTR_SX){}'.format(
	monet.CBBL, constrained.shape[0], DATA.shape[0], monet.CEND
))
pInter.to_csv(path.join(PT_OUT, 'DTA_FLTR_SX.csv'), index=False)
