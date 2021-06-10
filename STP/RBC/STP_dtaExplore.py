import sys
import random
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
    (USR, LND, AOI, QNT) = ('dsk', 'PAN', 'HLT', '50')
else:
    (USR, LND, AOI, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
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
(sexLim, renLim, resLim) = (2, 8, .3)
# Goals constraints -----------------------------------------------------------
cptLim = (-1, .1)
poeLim = (.9, 1)
ttiLim = (0, 30*2)
ttoLim = (4*365, 6*365)
wopLim = (4*365, 6*365)
# Filter and return dataframe -------------------------------------------------
constrained = DATA[
    (cptLim[0] <= DATA['CPT']) & (DATA['CPT'] <= cptLim[1]) &
    (wopLim[0] <= DATA['WOP']) & (DATA['WOP'] <= wopLim[1]) &
    (ttiLim[0] <= DATA['TTI']) & (DATA['TTI'] <= ttiLim[1]) &
    (ttoLim[0] <= DATA['TTO']) & (DATA['TTO'] <= ttoLim[1]) &
    (poeLim[0] <= DATA['POE']) & (DATA['POE'] <= poeLim[1]) &
    (DATA['i_ren'] <= renLim)  & 
    (DATA['i_res'] <= resLim)  & 
    (DATA['i_sex'] == sexLim)  &
    (1e-5 <= (DATA['i_rsg'] + DATA['i_gsv']))
]
constrained
###############################################################################
# Export data
###############################################################################
constrained.to_csv(path.join(PT_OUT, 'DTA_FLTR.csv'), index=False)
###############################################################################
# Sex
###############################################################################
partA = DATA[(1500 < DATA['WOP']) & (DATA['i_sex'] == 2)]
partB = DATA[(500 > DATA['WOP'])  & (DATA['i_sex'] == 1)]
drops = ['TTI', 'TTO', 'POE', 'WOP', 'POF', 'CPT', 'i_sex']
dfs = [i.drop(drops, axis=1) for i in (partA, partB)]
inter = pd.merge(*dfs, 'inner')
constrained.to_csv(path.join(PT_OUT, 'DTA_sexInter.csv'), index=False)
