

import sys
import math
import numpy as np
from os import path
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans
import PGS_aux as aux
import PGS_gene as drv

if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'PGS', '50', 'HLT', '0.1', 'POE')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
# Params Scaling --------------------------------------------------------------
MAX_TIME = 365*2
###############################################################################
# Paths
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, fldr)
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img', 'heat')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
# Time and head -----------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_SUMS, PT_IMG, tS, 
    '{} DtaHeatmap [{}:{}:{}:{}]'.format(DRV, QNT, AOI, THS, MOI)
)
###############################################################################
# Select surface variables
###############################################################################
(scalers, HD_DEP, _, cmap) = aux.selectDepVars(MOI)
(ngdx, ngdy) = (1000, 1000)
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
###############################################################################
# Filter
###############################################################################
fltr = {
    'i_rei': 7,
    'i_pct': 0.90, 
    'i_pmd': 0.75, 
    'i_mtf': 0.75,
    'i_grp': 0.0
}
# Filter dataset for constraints ----------------------------------------------
cats = list(fltr.keys())
ks = [all(i) for i in zip(*[np.isclose(DATA[k], fltr[k]) for k in cats])]
dfFltr = DATA[ks]
# Filter dataset for outcome --------------------------------------------------
outs = [i for i in list(DATA.columns) if i[0]!='i']
poeDFRaw = dfFltr[dfFltr['POE']>=0]
# Feature creation ------------------------------------------------------------
poeDFRaw['mfr+fvb'] = poeDFRaw['i_mfr']+poeDFRaw['i_fvb']
poeDFRaw['ren*res'] = poeDFRaw['i_ren']*poeDFRaw['i_res']
poeDFRaw['POE_C'] = [math.floor(i*10) for i in poeDFRaw['POE']]
# Drop ranges -----------------------------------------------------------------
# poeDF = poeDFRaw.drop(labels=cats, axis=1).drop(labels=outs, axis=1)
###############################################################################
# Explore ranges
###############################################################################
poeDF = poeDFRaw[poeDFRaw['POE']>=0.75]
min(poeDF['i_ren'].unique())
min(poeDF['i_res'].unique())
sorted(poeDF['i_mfr'].unique())
sorted(poeDF['i_fvb'].unique())
###############################################################################
# Cluster
###############################################################################
# y_pred = KMeans(n_clusters=4).fit_predict(poeDF['POE'])
# poeDF['KMeans'] = y_pred
###############################################################################
# Matplotlib
###############################################################################
# COLORS = [
#     '#f7258570', '#b5179e65', '#7209b760', '#560bad55', '#480ca850',
#     '#3a0ca345', '#3f37c940', '#4361ee35', '#4895ef30', '#4cc9f025',
#     '#B4E9F120'
# ][::-1]
# jitter = np.random.normal(0, 0.01, size=(1, poeDF.shape[0]))[0]
# plt.scatter(
#     poeDF['mfr+fvb']+jitter, poeDF['ren*res'],
#     s=0.05, color=[COLORS[i] for i in poeDF['POE_C']]
# )
# plt.savefig(
#     path.join(path.dirname(path.realpath(__file__)), 'scatter.png'), 
#     dpi=500, bbox_inches='tight', transparent=False, pad_inches=0
# )

# COLORS = [
#     '#f7258550', '#b5179e50', '#7209b750', '#560bad50', '#480ca850',
#     '#3a0ca350', '#3f37c950', '#4361ee50', '#4895ef50', '#4cc9f050',
#     '#ECF9FD50'
# ][::-1]
# jitter = np.random.normal(0, 0.01, size=(1, poeDF.shape[0]))[0]
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(
#     poeDF['i_fvb']+jitter, poeDF['i_mfr']+jitter, poeDF['ren*res'],
#     s=0.05, color=[COLORS[i] for i in poeDF['POE_C']]
# )
# ax.show()
###############################################################################
# HTML
###############################################################################
jitter = np.random.normal(0, 0.01, size=(1, poeDF.shape[0]))[0]
poeDF['fvb'] = poeDF['i_fvb']+jitter
jitter = np.random.normal(0, 0.01, size=(1, poeDF.shape[0]))[0]
poeDF['mfr'] = poeDF['i_mfr']+jitter
# REN -------------------------------------------------------------------------
fig = go.Figure(data=go.Scatter3d(
    x=poeDF['fvb'], y=poeDF['mfr'], z=poeDF['i_ren'],
    customdata=np.dstack((poeDF['i_res']*10, poeDF['POE']))[0],
    mode='markers',
    marker=dict(
        size=2,
        color=poeDF['POE'],
        colorscale='Purples',
        opacity=0.35
    ),
    hovertemplate="fvb:%{x:.3f}<br>mfr:%{y:.3f}<br>ren:%{z:.3f}<br>res:%{customdata[0]:.3f}<br>POE:%{customdata[1]:.3f}"
))
fig.update_layout(
    scene = dict(
        xaxis_title='female viability (fvb)',
        yaxis_title='male fertility (mfr)',
        zaxis_title='number of releases (ren)',
    )
)
fig.write_html(path.join(PT_IMG, 'scatter-ren.html'))
# RES -------------------------------------------------------------------------
fig = go.Figure(data=go.Scatter3d(
    x=poeDF['fvb'], y=poeDF['mfr'], z=poeDF['i_res']*10,
    customdata=np.dstack((poeDF['i_ren'], poeDF['POE']))[0],
    mode='markers',
    marker=dict(
        size=2,
        color=poeDF['POE'],
        colorscale='Purples',
        opacity=0.35
    ),
    hovertemplate="fvb:%{x:.3f}<br>mfr:%{y:.3f}<br>res:%{z:.3f}<br>ren:%{customdata[0]:.3f}<br>POE:%{customdata[1]:.3f}"
))
fig.update_layout(
    scene = dict(
        xaxis_title='female viability (fvb)',
        yaxis_title='male fertility (mfr)',
        zaxis_title='size of releases [eggs/adult] (ren)',
    )
)
fig.write_html(path.join(PT_IMG, 'scatter-res.html'))
# REN*RES ---------------------------------------------------------------------
fig = go.Figure(data=go.Scatter3d(
    x=poeDF['fvb'], y=poeDF['mfr'], z=poeDF['ren*res']*10,
    customdata=np.dstack((poeDF['i_ren'], poeDF['i_res']*10, poeDF['POE']))[0],
    mode='markers',
    marker=dict(
        size=2,
        color=poeDF['POE'],
        colorscale='Purples',
        opacity=0.35
    ),
    hovertemplate="fvb:%{x:.3f}<br>mfr:%{y:.3f}<br>tot:%{z:.3f}<br>ren:%{customdata[0]:.3f}<br>res:%{customdata[1]:.3f}<br>POE:%{customdata[2]:.3f}"
))
fig.update_layout(
    scene = dict(
        xaxis = dict(nticks=5, range=[0, 0.5]),
        yaxis = dict(nticks=5, range=[0, 0.5]),
        zaxis = dict(nticks=5, range=[0, 10e3]),
        xaxis_title='female viability (fvb)',
        yaxis_title='male fertility (mfr)',
        zaxis_title='total released mosquitoes [eggs/adult] (ren*res)',
    )
)
fig.write_html(path.join(PT_IMG, 'scatter-ren_res.html'))