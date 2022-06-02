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
import tGD_aux as aux
import tGD_gene as drv
from more_itertools import locate
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

if monet.isNotebook():
    (USR, DRV, AOI, QNT, MTR, THS) = ('srv', 'linkedDrive', 'WLD', '50', 'WOP', '0.1')
else:
    (USR, DRV, AOI, QNT, MTR, THS) = sys.argv[1:]
EXPS = aux.EXPS
exp = EXPS[0]
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
###############################################################################
# Paths
###############################################################################
(drive, land) = (drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE), [[0], ])
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, exp, 'SUMMARY')
###############################################################################
# Read CSV
###############################################################################
thsStr = str(int(float(THS)*100))
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
    '{} DtaExplore [{}:{}:{}:{}]'.format('tGD', DRV, QNT, AOI, THS)
)
###############################################################################
# Filter Output with Constraints
###############################################################################
# Design constraints ----------------------------------------------------------
(renLim, resLim) = (25, 1.1)
# Goals constraints -----------------------------------------------------------
cptLim = (0.25, 1)
poeLim = (-.1, 1)
ttiLim = (-1, 365*5)
ttoLim = (-1, 6*365)
wopLim = (0, 10*365)
mnfLim = (-1, 1)
# Filter and return dataframe -------------------------------------------------
constrained = DATA[
    (cptLim[0] <= DATA['CPT']) & (DATA['CPT'] <= cptLim[1]) &
    (wopLim[0] <= DATA['WOP']) & (DATA['WOP'] <= wopLim[1]) &
    (ttiLim[0] <= DATA['TTI']) & (DATA['TTI'] <= ttiLim[1]) &
    (ttoLim[0] <= DATA['TTO']) & (DATA['TTO'] <= ttoLim[1]) &
    (poeLim[0] <= DATA['POE']) & (DATA['POE'] <= poeLim[1]) &
    (mnfLim[0] <= DATA['MNF']) & (DATA['MNF'] <= mnfLim[1]) &
    (DATA['i_ren'] <= renLim)  &
    (DATA['i_res'] <= resLim) 
]
constrained.shape
# Export data -----------------------------------------------------------------
print('{}* Found {}/{} matches (FLTR){}'.format(
	monet.CBBL, constrained.shape[0], DATA.shape[0], monet.CEND
))
constrained.to_csv(path.join(PT_OUT, 'DTA_FLTR.csv'), index=False)
constrained.to_csv(path.join(PT_OUT, 'DTA_FLTR_BD.csv'), index=False)
