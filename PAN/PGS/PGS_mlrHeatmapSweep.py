#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from os import path
import compress_pickle as pkl
from itertools import product
from datetime import datetime
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
import keras
from scikeras.wrappers import KerasRegressor
import PGS_aux as aux
import PGS_gene as drv

if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'PGS', '50', 'HLT', '0.1', 'POE')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
QNT = (None if QNT == 'None' else QNT)
MOD_SEL = 'krs'
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
# Params Scaling --------------------------------------------------------------
(xSca, ySca) = ('linear', 'linear')
TICKS_HIDE = False
MAX_TIME = 365*2
CLABEL_FONTSIZE = 0
thsStr = str(int(float(THS)*100))
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
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_OUT, tS, 
    '{} mlrHeatmap [{}:{}:{}]'.format(DRV, AOI, THS, MOI)
)
###############################################################################
# Load Model
###############################################################################
if QNT:
    fNameOut = '{}_{}Q_{}T_{}-{}-MLR'.format(
        AOI, int(QNT), int(float(THS)*100), MOI, MOD_SEL
    )
else:
    fNameOut = '{}_{}T_{}-{}-MLR'.format(AOI, int(float(THS)*100), MOI, MOD_SEL)
# Check for Keras model -------------------------------------------------------
if not (MOD_SEL == 'krs'):
    rf = pkl.load(path.join(PT_OUT, fNameOut+'.pkl'))
else:
    rf = keras.models.load_model(path.join(PT_OUT, fNameOut))
    # rf = KerasRegressor(reg)
    # rf.initialize(
    #     np.load(path.join(PT_OUT, 'X_train.npy')), 
    #     np.load(path.join(PT_OUT, 'y_train.npy'))
    # )
###############################################################################
# Sweep-Evaluate Model
###############################################################################
aren = list(np.arange(52, 20, -4))
alphas = np.geomspace(0.01, .75, len(aren))
(fig, ax) = plt.subplots(figsize=(10, 10))
for (ix, ren) in enumerate(aren):
    fltr = {
        'i_ren': [ren],
        'i_res': [25],
        'i_rei': [7],
        'i_pct': [0.90], 
        'i_pmd': [0.90], 
        'i_fvb': np.arange(0, .5, 0.0025), 
        'i_mtf': [0.75],
        'i_mfr': np.arange(0, .5, 0.0025)
    }
    fltrTitle = fltr.copy()
    # Assemble factorials ---------------------------------------------------------
    sweeps = [i for i in fltr.keys() if len(fltr[i])>1]
    [fltrTitle.pop(i) for i in sweeps]
    combos = list(zip(*product(fltr[sweeps[0]], fltr[sweeps[1]])))
    factNum = len(combos[0])
    for i in range(len(combos)):
        fltr[sweeps[i]] = combos[i]
    for k in fltr.keys():
        if len(fltr[k])==1:
            fltr[k] = fltr[k]*factNum
    # Generate probes -------------------------------------------------------------
    probeVct = np.array((
        fltr['i_ren'], fltr['i_res'], fltr['i_rei'],
        fltr['i_pct'], fltr['i_pmd'],
        fltr['i_mfr'], fltr['i_mtf'], fltr['i_fvb']
    )).T
    (x, y) = [list(i) for i in combos]
    z = rf.predict(probeVct)
    ###############################################################################
    # Generate response surface
    ###############################################################################
    (ngdx, ngdy) = (1000, 1000)
    scalers = [1, 1, 1]
    (xLogMin, yLogMin) = (
        min([i for i in sorted(list(set(x))) if i>0]),
        min([i for i in sorted(list(set(y))) if i>0])
    )
    rs = monet.calcResponseSurface(
        x, y, z, 
        scalers=scalers, mthd='cubic', 
        xAxis=xSca, yAxis=ySca,
        xLogMin=xLogMin, yLogMin=yLogMin,
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
        (zmin, zmax) = (0, 1)
        lvls = np.arange(zmin*1, zmax*1, (zmax-zmin)/20)
        cntr = [.5]
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
    xy = ax.plot(rsG[0], rsG[1], 'k.', ms=0.25, alpha=0.1, marker='.')
    cs = ax.contourf(
        rsS[0], rsS[1], rsS[2], 
        linewidths=0, alpha=alphas[ix],
        levels=lvls, colors=['#ffffff', '#8338EC'], extend='max'
    )
    cc = ax.contour(
        rsS[0], rsS[1], rsS[2], 
        levels=cntr, colors='#000000', # drive['colors'][-1][:-2], 
        linewidths=0.75, alpha=0.75, linestyles='solid'
    )
    # cs.cmap.set_over('red')
    cs.cmap.set_under('white')
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
    # Labels ------------------------------------------------------------------
    if not TICKS_HIDE:
        ax.set_xlabel(sweeps[0])
        ax.set_ylabel(sweeps[1])
        pTitle = ' '.join(['[{}: {}]'.format(i, fltrTitle[i][0]) for i in fltrTitle])
        plt.title(pTitle, fontsize=7.5)
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
    fig.tight_layout()
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    ax.set_facecolor("#00000000")
###############################################################################
# Export File
###############################################################################
# Generate filename -----------------------------------------------------------
(allKeys, fltrKeys) = (list(aux.DATA_SCA.keys()), set(fltrTitle.keys()))
fElements = []
for (i, k) in enumerate(allKeys):
    if k in fltrKeys:
        xEl = str(int(fltr[k][0]*aux.DATA_SCA[k])).zfill(aux.DATA_PAD[k])
    else:
        xEl = 'X'*aux.DATA_PAD[k]
    fElements.append(xEl)
fName = '{}_{}_{}-E_'.format(
        MOI, sweeps[0][2:], sweeps[1][2:]
    )+'_'.join(fElements)
fName = fName+'-{}Q_{}T'.format(QNT, thsStr)
# Save file -------------------------------------------------------------------
# print(path.join(PT_IMG, fName+'.png'))
print(path.join(PT_IMG, fName+'.png'))
fig.savefig(
    path.join(PT_IMG, fName+'.png'), 
    dpi=500, bbox_inches='tight', transparent=True, pad_inches=0
)
# Clearing and closing (fig, ax) ------------------------------------------
# plt.clf();plt.cla();plt.close(fig);plt.gcf()
