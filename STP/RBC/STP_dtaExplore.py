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
    PT_SUMS, PT_IMG, tS, 
    '{} ClsDICE [{}:{}:{}:{}]'.format(aux.XP_ID, aux.DRV, QNT, AOI, aux.THS)
)
###############################################################################
# DICE Plot 
###############################################################################
(sampleRate, shuffle) = (0.1, True)
ans = aux.DICE_PARS
pFeats = [
    ('i_sex', 'linear'), ('i_ren', 'linear'), ('i_res', 'linear'), 
    ('i_rsg', 'log'), ('i_gsv', 'log'), ('i_fcf', 'linear'), 
    ('i_hrm', 'linear'), ('i_hrt', 'linear')
]
# Filter dataset on specific features (drop others) ---------------------------
dataEffect = DATA[
    (DATA['i_ren'] > 0) & (DATA['i_res'] > 0) & 
    (DATA['i_grp'] == 0) & (DATA['i_mig'] == 0)
]
# Select rows to highlight on constraints ------------------------------------
dataHighlight = DATA[
    # ((DATA['i_rsg'] + DATA['i_gsv']) > 1e-5) & 
    (DATA['i_fcf'] > 1)
]
highRows = set(dataHighlight.index)
###############################################################################
# Iterate through AOI 
###############################################################################
(yVar, sigma, col) = ans[0]
for (yVar, sigma, col) in ans[:]:
    Parallel(n_jobs=JOB)(
        delayed(dbg.exportDICEParallel)(
            AOI, xVar, yVar, dataEffect, FEATS, PT_IMG, hRows=highRows,
            dpi=500, scale=scale, wiggle=True, sd=sigma, color=col, 
            sampleRate=sampleRate, hcolor='#00ff0029', lw=0.1, hlw=0.1
        ) for (xVar, scale) in pFeats
    )
# Export full panel -----------------------------------------------------------
cmd = [
    'inkscape', '--export-type=png', '--export-dpi=500', 
    path.join(PT_IMG, 'DICE.svg'), 
    '--export-filename='+path.join(PT_IMG, 'DICE.png')
]
subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
###############################################################################
# Filter Output with Constraints
###############################################################################
# cptLim = (-1, .25)
# poeLim = (-1, .1)
# ttiLim = (-10, 20*365)
# ttoLim = (-10, 20*365)
# wopLim = (-10, 20*365)
# # Filter and return dataframe -------------------------------------------------
# fltr = [
#     cptLim[0] <= DATA['CPT'], DATA['CPT'] <= cptLim[1],
#     wopLim[0] <= DATA['WOP'], DATA['WOP'] <= wopLim[1],
#     ttiLim[0] <= DATA['TTI'], DATA['TTI'] <= ttiLim[1],
#     ttoLim[0] <= DATA['TTO'], DATA['TTO'] <= ttoLim[1],
#     poeLim[0] <= DATA['POE'], DATA['POE'] <= poeLim[1],
# ]
# boolFilter = [all(i) for i in zip(*fltr)]
# daFltrd = DATA[boolFilter]
# daFltrd


# cols = ('i_rsg', 'i_rer', 'i_ren', 'i_qnt', 'i_gsv', 'i_fic', LABLS[0])
# x = df[[*cols]].values
# min_max_scaler = preprocessing.MinMaxScaler()
# x_scaled = min_max_scaler.fit_transform(x)
# df = pd.DataFrame(x_scaled, columns=cols)
# gsv = list(df['i_gsv'].unique())
# dfFltrd = df[df['i_gsv']==gsv[-1]]
# ###############################################################################
# # Load Dataset
# ###############################################################################
# fig = px.scatter_3d(
#     dfFltrd, 
#     x='i_rer', y='i_ren', z='i_fic', 
#     size=list(1*np.asarray(dfFltrd['i_rsg'])),
#     color=LABLS[0], 
#     opacity=.1, color_continuous_scale='purples_r'
# )
# fig.update_traces(
#     marker=dict(
#         # size=2, 
#         line=dict(width=0, color=(0,0,0,0))
#     )
# )
# fig.show()
