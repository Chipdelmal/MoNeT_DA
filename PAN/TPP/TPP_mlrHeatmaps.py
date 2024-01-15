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
(xSca, ySca) = ('linear', 'linear')
(ngdx, ngdy) = (1000, 1000)
scalers = [1, 1, 1]
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
#   [0] shc: 0.75 - 1.00
#   [1] sbc: 0.80 - 1.00
#   [2] hdr: 0.80 - 1.00
#   [3] rgr: 0.00 - 0.20
#   [4] inf: 0.00 - 0.25
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
delta = 0.001
(shcRan, sbcRan, rgrRan, hdrRan, infRan) = (
    np.arange(0.75, 1.00+delta, delta),
    np.arange(0.80, 1.00+delta, delta),
    np.arange(0.00, 0.20+delta, delta),
    np.array([0.80]),
    np.array([0.00])
)
combos = np.array(list(product(*[shcRan, sbcRan, hdrRan, rgrRan, infRan])))
pred = rf.predict(combos)
# if MOI=='WOP':
#     pred = pred*aux.XRAN[1]/365
###############################################################################
# Generate response surface
###############################################################################
(x, y, z) = (list(combos.T[3]), list(combos.T[1]), pred)
(xMin, yMin) = (
    min([i for i in sorted(list(set(x))) if i>0]),
    min([i for i in sorted(list(set(y))) if i>0])
)
rs = monet.calcResponseSurface(
    x, y, z, 
    scalers=(1, 1, 1), mthd='linear', 
    xAxis=xSca, yAxis=ySca,
    xLogMin=xMin, yLogMin=yMin,
    DXY=(ngdx, ngdy)
)
###############################################################################
# Levels and Ranges
###############################################################################
# Get ranges ------------------------------------------------------------------
(a, b) = ((min(x), max(x)), (min(y), max(y)))
(ran, rsG, rsS) = (rs['ranges'], rs['grid'], rs['surface'])
# Contour levels --------------------------------------------------------------
if MOI == 'WOP':
    (zmin, zmax) = (0, 0.025)
    lvls = np.arange(zmin*1, zmax*1, (zmax-zmin)/20)
    cntr = [0.15]
elif MOI == 'CPT':
    (zmin, zmax) = (0, 1)
    lvls = np.arange(zmin*1, zmax*1, (zmax-zmin)/20)
    cntr = [.9]
elif MOI == 'POE':
    (zmin, zmax) = (0, 1)
    lvls = np.arange(zmin*1, zmax*1, (zmax-zmin)/10)
    cntr = [.9]
    lvls = [cntr[0]-.00001, cntr[0]]
(scalers, HD_DEP, _, cmap) = aux.selectDepVars(MOI)
###############################################################################
# Plot
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 10))
xy = ax.plot(rsG[0], rsG[1], 'k.', ms=1, alpha=0.25, marker='1')
cc = ax.contour(
    rsS[0], rsS[1], rsS[2], 
    levels=lvls, colors='#2b2d42', # drive['colors'][-1][:-2], 
    linewidths=2, alpha=.9, linestyles='solid'
)
cs = ax.contourf(
    rsS[0], rsS[1], rsS[2], 
    linewidths=0,
    levels=lvls, cmap=cmap, extend='max'
)
cs.cmap.set_under('white')