import sys
import numpy as np
from os import path
import pandas as pd
import compress_pickle as pkl
from datetime import datetime
import matplotlib.pyplot as plt
from itertools import product
import MoNeT_MGDrivE as monet
import PGS_aux as aux
import PGS_gene as drv
import PGS_mlrMethods as mth

if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'PGS', '50', 'HLT', '0.1', 'WOP')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
iVars = ['i_fvb', 'i_mfr']
# iVars = ['i_ren', 'i_res', 'i_fvb']
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
# Params Scaling --------------------------------------------------------------
(xSca, ySca) = ('linear', 'linear')
TICKS_HIDE = True
MAX_TIME = 365*2
CLABEL_FONTSIZE = 0
(HD_IND) = ([iVars[0], iVars[1]]) 
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
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_OUT, tS, 
    '{} mlrHeatmap [{}:{}:{}]'.format(DRV, AOI, THS, MOI)
)
###############################################################################
# Select Model and Scores
###############################################################################
(MOD_SEL, K_SPLITS, T_SIZE) = ('mlp', 10, .1)
###############################################################################
# Load Model
###############################################################################
fNameOut = '{}_{}T_{}-{}-MLR'.format(AOI, int(float(THS)*100), MOI, MOD_SEL)
rf = pkl.load(path.join(PT_OUT, fNameOut+'.pkl'))
###############################################################################
# Sweep-Evaluate Model
###############################################################################
fltr = {
    'i_ren': [25.0],
    'i_res': [50.0],
    'i_rei': [7],
    'i_pct': [1.00], 
    'i_pmd': [1.00], 
    'i_mfr': np.arange(0, .3, 0.01), 
    'i_mtf': [0.75],
    'i_fvb': np.arange(0, .3, 0.01)
}
# Assemble factorials ---------------------------------------------------------
sweeps = [i for i in fltr.keys() if len(fltr[i])>1]
combos = list(zip(*product(fltr[sweeps[0]], fltr[sweeps[1]])))
factNum = len(combos[0])
for i in range(len(combos)):
    fltr[sweeps[i]] = combos [i]
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
    min([i for i in sorted(list(set(x))) if i > 0]),
    min([i for i in sorted(list(set(y))) if i > 0])
)
rs = monet.calcResponseSurface(
    x, y, z, 
    scalers=scalers, mthd='linear', 
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
if MOI == 'TTI':
    (zmin, zmax) = (0, 365*5)
    lvls = np.arange(zmin*1, zmax*1, (zmax-zmin)/20)
    cntr = [2*365]
if MOI == 'TT0':
    (zmin, zmax) = (0, 365*5)
    lvls = np.arange(zmin*1, zmax*1, (zmax-zmin)/20)
    cntr = [2*365]
elif MOI == 'WOP':
    (zmin, zmax) = (0, 1)
    lvls = np.arange(zmin*1, zmax*1, (zmax-zmin)/20)
    cntr = [.5]
    lvls = [cntr[0]-1, cntr[0]]
elif MOI == 'CPT':
    (zmin, zmax) = (-.05, 1.05)
    lvls = np.arange(zmin*1, zmax*1, (zmax-zmin)/20)
    cntr = [.5]
elif MOI == 'POE':
    (zmin, zmax) = (0.1, 1.05)
    lvls = np.arange(zmin*1, zmax*1, (zmax-zmin)/20)
    cntr = [.9]
    lvls = [cntr[0]-.01, cntr[0]]
(scalers, HD_DEP, _, cmap) = aux.selectDepVars(MOI)
###############################################################################
# Plot
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 8))
xy = ax.plot(rsG[0], rsG[1], 'k.', ms=2.5, alpha=.25, marker='.')
cc = ax.contour(
    rsS[0], rsS[1], rsS[2], 
    levels=cntr, colors=drive['colors'][-1][:-2], 
    linewidths=3, alpha=.825, linestyles='solid'
)
cs = ax.contourf(
    rsS[0], rsS[1], rsS[2], 
    levels=lvls, cmap=cmap, extend='max'
)
# cs.cmap.set_over('red')
cs.cmap.set_under('white')