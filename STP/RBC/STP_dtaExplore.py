import sys
import random
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
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd


if monet.isNotebook():
    (USR, LND, AOI, QNT) = ('dsk', 'PAN', 'HLT', '50')
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
    [i for i in COLS if i[0]=='i'],
    [i for i in COLS if i[0]!='i']
)
###############################################################################
# PDP/ICE Plot 
###############################################################################
(sampleRate, shuffle) = (1, True)
ans = (
    ('CPT', 0.01, '#4361ee43'), ('WOP', 0.25, '#ff006e12'), 
    ('TTI', 0.25, '#be0aff13'), ('TTO', 0.25, '#a1ef7a43'), 
    ('POE', 0.01, '#23194212')
)
pFeats = [
    ('i_sex', 'linear'), ('i_ren', 'linear'), ('i_res', 'linear'), 
    ('i_rsg', 'log'), ('i_gsv', 'log'), ('i_fcf', 'linear')
]
# Iterate through AOI ---------------------------------------------------------
ix = 0
(yVar, sigma, col) = ans[ix]
dataEffect = DATA[
    (DATA['i_ren'] > 0) & (DATA['i_res'] > 0) & 
    (DATA['i_grp'] == 0) & (DATA['i_mig'] == 0)
]
# Get factorials --------------------------------------------------------------
(xVar, scale) = pFeats[1]
for (xVar, scale) in pFeats:
    fName = path.join(PT_IMG, 'DICE_{}_{}.png'.format(xVar[2:], yVar))
    aux.plotDICE(
        dataEffect, xVar, yVar, FEATS,
        scale=scale, wiggle=True, sd=sigma, color=col
    )
    # # Plot figure -------------------------------------------------------------
    # (fig, ax) = plt.subplots(figsize=(10, 10))
    # for i in range(0, dropFeats.shape[0]):
    #     entry = dropFeats.iloc[i]
    #     if (random.uniform(0, 1) <= sampleRate):
    #         zipIter = zip(list(entry.keys()), list(entry.values))
    #         fltrRaw = [list(dataEffect[col] == val) for (col, val) in zipIter]
    #         fltr = [all(i) for i in zip(*fltrRaw)]
    #         data = dataEffect[fltr][[xVar, yVar]]
    #         if shuffle:
    #             yData = [
    #                 i+np.random.uniform(low=-sigma, high=sigma) for i in data[yVar]
    #             ]
    #         else:
    #             yData = data[yVar]
    #         # Plot ------------------------------------------------------------
    #         ax.plot(data[xVar], yData, lw=.175, color=col)
    # # Log and linear scales ---------------------------------------------------
    # if scale == 'log':
    #     xRan = [xLvls[1], xLvls[-1]]
    # else:
    #     xRan = [xLvls[0], xLvls[-1]]
    # STYLE = {
    #     'xRange': xRan,
    #     'yRange': [min(outFact)*.975, max(outFact)*1.025]
    # }
    # ax.set_aspect(monet.scaleAspect(1, STYLE))
    # ax.set_xlim(STYLE['xRange'])
    # ax.set_ylim(STYLE['yRange'])
    # ax.set_xscale(scale)
    # ax.vlines(
    #     xLvls, 0, 1, lw=.25, ls='--', color='#000000', 
    #     transform = ax.get_xaxis_transform()
    # )
    # plt.xticks(fontsize=20)
    # plt.yticks(fontsize=20, rotation=90)
    # fig.tight_layout()
    fig.savefig(fName, dpi=500, bbox_inches='tight', pad=0)
    plt.close('all')
###############################################################################
# Filter Output with Constraints
###############################################################################
cptLim = (.8, 1.25)
poeLim = (-1, .1)
ttiLim = (-10, 20*365)
ttoLim = (-10, 20*365)
wopLim = (-10, 20*365)
# Filter and return dataframe -------------------------------------------------
fltr = [
    cptLim[0] <= DATA['CPT'], DATA['CPT'] <= cptLim[1],
    wopLim[0] <= DATA['WOP'], DATA['WOP'] <= wopLim[1],
    ttiLim[0] <= DATA['TTI'], DATA['TTI'] <= ttiLim[1],
    ttoLim[0] <= DATA['TTO'], DATA['TTO'] <= ttoLim[1],
    poeLim[0] <= DATA['POE'], DATA['POE'] <= poeLim[1],
]
boolFilter = [all(i) for i in zip(*fltr)]
daFltrd = DATA[boolFilter]
daFltrd


cols = ('i_rsg', 'i_rer', 'i_ren', 'i_qnt', 'i_gsv', 'i_fic', LABLS[0])
x = df[[*cols]].values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df = pd.DataFrame(x_scaled, columns=cols)
gsv = list(df['i_gsv'].unique())
dfFltrd = df[df['i_gsv']==gsv[-1]]
###############################################################################
# Load Dataset
###############################################################################
fig = px.scatter_3d(
    dfFltrd, 
    x='i_rer', y='i_ren', z='i_fic', 
    size=list(1*np.asarray(dfFltrd['i_rsg'])),
    color=LABLS[0], 
    opacity=.25, color_continuous_scale='purples_r'
)
fig.update_traces(
    marker=dict(
        # size=2, 
        line=dict(width=0, color=(0,0,0,0))
    )
)
fig.show()
