#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 
import sys
import numpy as np
from os import path
import pandas as pd
from itertools import product
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from keras.models import load_model
import MoNeT_MGDrivE as monet
import TPP_aux as aux
import TPP_gene as drv
import TPP_mlrMethods as mth

if monet.isNotebook():
    (USR, LND, EXP, DRV, AOI, QNT, THS, MOI) = (
        'zelda', 
        'BurkinaFaso', 'highEIR', 
        'HUM', 'CSS', '50', '0.25', 'WOP'
    )
else:
    (USR, LND, EXP, DRV, AOI, QNT, THS, MOI) = sys.argv[1:]
    QNT = (None if (QNT=='None') else QNT)
# Setup number of threads -----------------------------------------------------
(DATASET_SAMPLE, VERBOSE, JOB, FOLDS, SAMPLES) = (1, 0, 20, 2, 1000)
CHUNKS = JOB
DEV = False
C_VAL = True
###############################################################################
# Paths
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, EXP)
PT_OUT = path.join(PT_ROT, 'ML')
PT_OUT_THS = path.join(PT_ROT, f'ML{int(float(THS)*100)}')
PT_IMG = path.join(PT_OUT, 'img')
PT_IMG_THS = path.join(PT_OUT_THS, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG, PT_OUT_THS, PT_IMG_THS]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_OUT_THS, tS, 
    '{} mlrTrainKeras [{}:{}:{}:{}]'.format(DRV, AOI, QNT, THS, MOI)
)
###############################################################################
# Read Dataframe
###############################################################################
if QNT:
    fName = 'SCA_{}_{}Q_{}T.csv'.format(AOI, int(QNT), int(float(THS)*100))
else:
    fName = 'SCA_{}_{}T_MLR.csv'.format(AOI, int(float(THS)*100))
df = pd.read_csv(path.join(PT_OUT, fName))
###############################################################################
# Read Model
###############################################################################
modID = 'krs'
fNameOut = '{}_{}Q_{}T_{}-{}-MLR'.format(
    AOI, int(QNT), int(float(THS)*100), MOI, modID
)
mdlPath = path.join(PT_OUT_THS, fNameOut)
rf = load_model(mdlPath)
###############################################################################
# Evaluate Model
#   shc: 0.75 - 1.00
#   sbc: 0.80 - 1.00
#   hdr: 0.80 - 1.00
#   rgr: 0.00 - 0.20
#   inf: 0.00 - 0.25
###############################################################################
pVect = np.array([
    [0.75, 0.85, 1, 0, 0],
    [1.00, 0.80, 1, 0, 0]
])
pred = rf.predict(pVect)
if MOI=='WOP':
    pred = pred*aux.XRAN[1]/365
print(pred)
###############################################################################
# Factorial Evaluation of Model
###############################################################################
delta = 0.01
(shcRan, sbcRan, rgrRan, hdrRan, infRan) = (
    np.arange(0.75, 1.00+delta, delta),
    np.arange(0.80, 1.00+delta, delta),
    np.arange(0.00, 0.20+delta, delta),
    np.array([0.80]),
    np.array([0.00])
)
combos = np.array(list(product(*[shcRan, sbcRan, hdrRan, rgrRan, infRan])))
pred = rf.predict(combos)
if MOI=='WOP':
    pred = pred*aux.XRAN[1]/365
###############################################################################
# 3D Plot Results
###############################################################################   
yearsFilter = 1
fltr = np.array([1 if (i>=yearsFilter) else 0 for i in pred.T[0]])
fig = go.Figure(data=go.Scatter3d(
    x=combos[np.where(fltr)][:,1], 
    y=combos[np.where(fltr)][:,3], 
    z=combos[np.where(fltr)][:,0],
    customdata=pred[np.where(fltr)],
    mode='markers',
    marker=dict(
        size=5,
        color=pred.T[0][np.where(fltr)],
        colorscale='Purples',
        opacity=0.35,
        cmin=yearsFilter,
        cmax=3
    ),
    hovertemplate="sbc:%{x:.3f}<br>rgr:%{y:.3f}<br>shc:%{z:.3f}<br>MOI:%{customdata:.3f}"
))
fig.update_layout(
    scene_aspectmode='cube', # 'cube',
    scene = dict(
        xaxis_title='sbc',
        yaxis_title='rgr',
        zaxis_title='shc',
        xaxis = dict(nticks=4, range=[0.80, 1.00],),
        yaxis = dict(nticks=4, range=[0.00, 0.20],),
        zaxis = dict(nticks=4, range=[0.80, 1.00],)
    )
)
# fig.write_html(path.join(PT_IMG_THS, fNameOut+'.html'))
fig.write_html(path.join('./tmp/', fNameOut+'.html'))


