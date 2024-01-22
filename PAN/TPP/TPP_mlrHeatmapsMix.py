#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 
import sys
import numpy as np
from os import path
import pandas as pd
from itertools import product
import matplotlib.pyplot as plt
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
        'HUM', 'MRT', '50', '0.25', 'WOP'
    )
else:
    (USR, LND, EXP, DRV, AOI, QNT, THS, MOI) = sys.argv[1:]
    QNT = (None if (QNT=='None') else QNT)
HDR_PAR = 0.80
# Setup number of threads -----------------------------------------------------
(DATASET_SAMPLE, VERBOSE, JOB, FOLDS, SAMPLES) = (1, 0, 20, 2, 1000)
CHUNKS = JOB
DEV = False
C_VAL = True
delta = 0.005
# Heatmap parameters ----------------------------------------------------------
(xSca, ySca) = ('linear', 'linear')
(ngdx, ngdy) = (1000, 1000)
scalers = [1, 1, 1]
YEAR_THS = 2
TICKS_HIDE = True
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
PT_IMG_THS = path.join(PT_OUT_THS, 'img', 'heatmaps')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG, PT_OUT_THS, PT_IMG_THS]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_OUT_THS, tS, 
    '{} mlrHeatmaps [{}:{}:{}:{}]'.format(DRV, AOI, QNT, THS, MOI)
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
# pVect = np.array([
#     [1.00, 0.85, 1, 0, 0],
#     [1.00, 0.80, 1, 0, 0]
# ])
# pred = rf.predict(pVect)
# if MOI=='WOP':
#     pred = pred*aux.XRAN[1]/365
# print(pred)
###############################################################################
# Factorial Evaluation of Model
###############################################################################
(SHC_RAN, INF_RAN) = (
    np.arange(0.75, 1.01, .025),
    np.arange(0, .31, .025)
)
(ix, jx) = (-3, 0)
for jx in range(len(INF_RAN)):
    (shcRan, sbcRan, rgrRan, hdrRan, infRan) = (
        np.arange(0.75, 1.00+delta, delta),
        np.arange(0.80, 1.00+delta, delta),
        np.arange(0.00, 0.20+delta, delta),
        np.array([HDR_PAR]),
        np.array([INF_RAN[jx]])
    )
    combos = np.array(list(product(*[shcRan, sbcRan, hdrRan, rgrRan, infRan])))
    pred = rf.predict(combos, verbose=0)
    if MOI=='WOP':
        pred = pred*aux.XRAN[1]/365
    ###############################################################################
    # Generate response surface
    ###############################################################################
    (x, y, z) = (
        list(combos.T[1]+combos.T[3]),
        list(combos.T[0]),  
        pred
    )
    (xMin, yMin) = (
        min([i for i in sorted(list(set(x))) if (i>0)]),
        min([i for i in sorted(list(set(y))) if (i>0)])
    )
    rs = monet.calcResponseSurface(
        x, y, z, 
        scalers=(1, 1, 1), mthd='nearest', 
        xAxis=xSca, yAxis=ySca,
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
        (zmin, zmax) = (0, 5.5)
        lvls = np.arange(zmin*1, zmax*1, (zmax-zmin)/5.5)
        cntr = [YEAR_THS]
    elif MOI == 'CPT':
        (zmin, zmax) = (0, 1)
        lvls = np.arange(zmin*1, zmax*1.1, (zmax-zmin)/5)
        cntr = [.75]
    elif MOI == 'POE':
        (zmin, zmax) = (0, 1)
        lvls = np.arange(zmin*1, zmax*1.1, (zmax-zmin)/10)
        cntr = [.9]
        lvls = [cntr[0]-.00001, cntr[0]]
    (scalers, HD_DEP, _, _) = aux.selectDepVars(MOI)
    if AOI=='HLT':
        cmap = monet.generateAlphaColorMapFromColor('#ff006eEE')
    elif AOI=='CSS':
        cmap = monet.generateAlphaColorMapFromColor('#03045eEE')
    elif AOI=='MRT':
        cmap = monet.generateAlphaColorMapFromColor('#8338ecEE')
    elif AOI=='PRV':
        cmap = monet.generateAlphaColorMapFromColor('#3a6ea5EE')
    else:
        cmap = monet.generateAlphaColorMapFromColor('#ffb3c6EE')
    ###############################################################################
    # Plot
    ###############################################################################
    (fig, ax) = plt.subplots(figsize=(10, 10))
    xy = ax.plot(rsG[0], rsG[1], 'k.', ms=1, alpha=0.25, marker='1')
    cc = ax.contour(
        rsS[0], rsS[1], rsS[2], 
        levels=lvls, colors='#2b2d42',
        linewidths=2, alpha=.85, linestyles='solid'
    )
    if not TICKS_HIDE:
        ax.clabel(cc, cc.levels, inline=True, fontsize=10)
    cs = ax.contourf(
        rsS[0], rsS[1], rsS[2], 
        linewidths=0,
        levels=lvls, cmap=cmap, extend='max',
        vmin=YEAR_THS-1
    )
    cs.cmap.set_under('#ffffff00')
    # Color bar ---------------------------------------------------------------
    if not TICKS_HIDE:
        cbar = fig.colorbar(cs)
        cbar.ax.get_yaxis().labelpad = 25
        cbar.ax.set_ylabel('{}'.format(MOI), fontsize=15, rotation=270)
    # Grid and ticks ----------------------------------------------------------
    if xSca == 'log':
        gZeroX = [i for i in list(sorted(set(x))) if i>0] 
        ax.set_xticks([i/scalers[0] for i in gZeroX])
        ax.axes.xaxis.set_ticklabels(gZeroX)
    else:
        ax.set_xticks([i/scalers[0] for i in list(sorted(set(x)))])
        ax.axes.xaxis.set_ticklabels(sorted(set(x)))
    if ySca == 'log':
        gZeroY = [i for i in list(sorted(set(y))) if i>0] 
        ax.set_yticks([i/scalers[1] for i in gZeroY])
        ax.axes.yaxis.set_ticklabels(gZeroY)
    else:
        ax.set_yticks([i/scalers[1] for i in list(sorted(set(y)))])
        ax.axes.yaxis.set_ticklabels(sorted(set(y)))
    ax.grid(which='major', axis='x', lw=.1, alpha=0.3, color=(0, 0, 0))
    ax.grid(which='major', axis='y', lw=.1, alpha=0.3, color=(0, 0, 0))
    # Axes scales and limits --------------------------------------------------
    ax.set_xscale(xSca)
    ax.set_yscale(ySca)
    plt.xlim(ran[0][0], ran[0][1])
    plt.ylim(ran[1][0], ran[1][1])
    if TICKS_HIDE:
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
        # ax.axes.xaxis.set_visible(False)
        # ax.axes.yaxis.set_visible(False)
        ax.xaxis.set_tick_params(width=0)
        ax.yaxis.set_tick_params(width=0)
        ax.tick_params(
            left=False, labelleft=False, bottom=False, labelbottom=False
        )
        ax.set_axis_off()
    else:
        ax.set_xlabel("rgr + sbc")
        ax.set_ylabel("shc")
    fig.tight_layout()
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    ax.set_facecolor("#00000000")
    ###############################################################################
    # Export File
    ###############################################################################
    # Generate filename -----------------------------------------------------------
    (shcName, sbcName, hdrName, rgrName, infName) = (
        str(int(shcRan[0]*aux.DATA_SCA['i_shc'])).zfill(aux.DATA_PAD['i_shc']),
        str(int(sbcRan[0]*aux.DATA_SCA['i_sbc'])).zfill(aux.DATA_PAD['i_sbc']),
        str(int(hdrRan[0]*aux.DATA_SCA['i_hdr'])).zfill(aux.DATA_PAD['i_hdr']),
        str(int(rgrRan[0]*aux.DATA_SCA['i_rgr'])).zfill(aux.DATA_PAD['i_rgr']),
        str(int(infRan[0]*aux.DATA_SCA['i_inf'])).zfill(aux.DATA_PAD['i_inf'])
    )
    fName = f'E_X_X_{hdrName}_X_{infName}'
    # fName = fName+'-{}_{}_{}Q_{}T-ALT'.format(AOI, MOI, QNT, str(int(float(THS)*100)))
    fName = fName+'-{}_{}_{}Q-ALT'.format(AOI, MOI, QNT)
    # fig.savefig(
    #     path.join('./tmp/', f'{fName}.png'), 
    #     dpi=500, bbox_inches='tight', transparent=True, pad_inches=0
    # )
    fig.savefig(
        path.join(PT_IMG_THS, f'{fName}.png'), 
        dpi=500, bbox_inches='tight', transparent=True, pad_inches=0
    )
    plt.close('all')
        
        
# E_01050_X_00800_X_0015000-HLT_WOP_50Q_25T