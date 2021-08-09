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
    (USR, LND, AOI, DRV, QNT) = ('lab', 'PAN', 'HLT', 'LDR', '50')
else:
    (USR, LND, AOI, DRV, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
TRACE_NUM = 30000
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
    PT_SUMS, PT_IMG, tS,
    '{} ClsDICE [{}:{}:{}:{}]'.format(aux.XP_ID, aux.DRV, QNT, AOI, aux.THS)
)
###############################################################################
# DICE Plot
###############################################################################
(sampleRate, shuffle) = (TRACE_NUM/DATA.shape[0], True)
ans = aux.DICE_PARS
pFeats = [
    ('i_sex', 'linear'), ('i_ren', 'linear'), ('i_res', 'linear'),
    ('i_rsg', 'log'),    ('i_gsv', 'log'),
    ('i_fch', 'linear'), ('i_fcb', 'linear'), ('i_fcr', 'linear'),
    ('i_hrm', 'linear'), ('i_hrf', 'linear'),
]
# Filter dataset on specific features (drop others) ---------------------------
dataEffect = DATA[
    (DATA['i_ren'] > 0) & (DATA['i_res'] > 0) &
    (DATA['i_grp'] == 0) & (DATA['i_mig'] == 0)
]
# Select rows to highlight on constraints ------------------------------------
dataHighlight = DATA[
    ((DATA['i_rsg'] + DATA['i_gsv']) > 1e-5) & 
    (DATA['i_fch'] > .8) & (DATA['i_fcr'] > .8)
]
highRows = set([]) # set(dataHighlight.index)
###############################################################################
# Iterate through AOI
###############################################################################
(yVar, sigma, col, yRange) = ans[0]
for (yVar, sigma, col, yRange) in ans[:]:
    Parallel(n_jobs=JOB)(
        delayed(dbg.exportDICEParallel)(
            AOI, xVar, yVar, dataEffect, FEATS, PT_IMG, hRows=highRows,
            dpi=400, scale=scale, wiggle=True, sd=sigma, sampleRate=sampleRate,
            color=col, hcolor='#000000'+'50', lw=0.1, hlw=0.075, yRange=yRange,
            ticksHide=True
        ) for (xVar, scale) in pFeats
    )
# Export full panel -----------------------------------------------------------
cmd = [
    'inkscape', '--export-type=png', '--export-dpi=400',
    path.join(PT_IMG, 'DICE.svg'),
    '--export-filename='+path.join(PT_IMG, 'DICE.png')
]
subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
