import sys
from math import exp
from os import minor, path
from re import match
from glob import glob
from itertools import product
from joblib import dump, load
from datetime import datetime
import numpy as np
from numpy.lib.arraypad import pad
import pandas as pd
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
from more_itertools import locate
from sklearn.model_selection import ParameterGrid
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

if monet.isNotebook():
    (USR, LND, AOI, DRV, QNT, MOI) = ('dsk', 'PAN', 'HLT', 'LDR', '50', 'WOP')
else:
    (USR, LND, AOI, DRV, QNT, MOI) = (
        sys.argv[1], sys.argv[2], sys.argv[3], 
        sys.argv[4], sys.argv[5], sys.argv[6]
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
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND, DRV)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img', 'heat')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
###############################################################################
# Select surface variables
###############################################################################
(HD_IND, kSweep) = (
    ['i_fch', 'i_fcb'], 'i_res'
)
(xSca, ySca) = ('linear', 'linear')
# Scalers and sampling --------------------------------------------------------
(scalers, HD_DEP, _, cmap) = aux.selectDepVars(MOI, AOI)
(ngdx, ngdy) = (1000, 1000)
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
(zmin, zmax) = (min(DATA[MOI]), max(DATA[MOI]))
# (zmin, zmax) = (-0.1, max(DATA[MOI]))
(lvls, mthd) = (np.arange(zmin*.9, zmax*1.1, (zmax-zmin)/20), 'linear')
# (lvls, mthd) = (np.arange(-0.1, 1.1, 1.5/20), 'nearest')
# Filter the dataframe --------------------------------------------------------
headerInd = [i for i in DATA.columns if i[0]=='i']
uqVal = {i: list(DATA[i].unique()) for i in headerInd}
# Filter the dataframe --------------------------------------------------------
amend = uqVal
amend['i_res'] = [0]
amendFact = list(ParameterGrid(amend))
outFix = {
    'TTI': max(DATA['TTI']), 'TTO': max(DATA['TTO']), 'WOP': min(DATA['WOP']),
    'POE': min(DATA['POE']), 'POF': max(DATA['POF']), 'CPT': max(DATA['CPT']),
    'MNF': max(DATA['MNF'])
}
amendDict = [{**i, **outFix} for i in amendFact]
DATA = DATA.append(amendDict, ignore_index=True)
# Filter the dataframe --------------------------------------------------------
headerInd = [i for i in DATA.columns if i[0]=='i']
uqVal = {i: list(DATA[i].unique()) for i in headerInd}
###############################################################################
# Filter dataframe
###############################################################################
fltr = {
    'i_sex': 2,
    'i_ren': 8,
    'i_res': .6,
    'i_rsg': 0.079,
    'i_gsv': 1.e-02,
    'i_fch': 0.175,
    'i_fcb': 0.117,
    'i_fcr': 0,
    'i_hrm': 1.0,
    'i_hrf': 0.956,
    'i_grp': 0, 'i_mig': 0
}
[fltr.pop(i) for i in HD_IND]
# Sweep over values -----------------------------------------------------------
sweep = uqVal[kSweep]
for sw in sweep:
    fltr[kSweep] = sw
    ks = [all(i) for i in zip(*[DATA[k]==fltr[k] for k in list(fltr.keys())])]
    dfSrf = DATA[ks]
    if dfSrf.shape[0] < 4:
        continue
    ###########################################################################
    # Generate Surface
    ###########################################################################
    (x, y, z) = (dfSrf[HD_IND[0]], dfSrf[HD_IND[1]], dfSrf[MOI])
    scalers = [1, 1, 1] # max(x), 1, 1] # max(y), 1]
    (xLogMin, yLogMin) = (
        min([i for i in sorted(list(x.unique())) if i > 0]),
        min([i for i in sorted(list(y.unique())) if i > 0])
    )
    rs = monet.calcResponseSurface(
        x, y, z, 
        scalers=scalers, mthd=mthd, 
        xAxis=xSca, yAxis=ySca,
        xLogMin=xLogMin, yLogMin=yLogMin,
        DXY=(ngdx, ngdy)
    )
    # Get ranges --------------------------------------------------------------
    (a, b) = ((min(x), max(x)), (min(y), max(y)))
    (ran, rsG, rsS) = (rs['ranges'], rs['grid'], rs['surface'])
    ###########################################################################
    # Plot
    ###########################################################################
    (fig, ax) = plt.subplots(figsize=(10, 8))
    # Experiment points, contour lines, response surface ----------------------
    xy = ax.plot(rsG[0], rsG[1], 'k.', ms=2.5, alpha=.25, marker='.')
    cc = ax.contour(rsS[0], rsS[1], rsS[2], levels=lvls, colors='w', linewidths=.5, alpha=.25)
    cs = ax.contourf(rsS[0], rsS[1], rsS[2], levels=lvls, cmap=cmap, extend='max')
    # cs.cmap.set_over('red')
    # cs.cmap.set_under('blue')
    # Color bar ---------------------------------------------------------------
    cbar = fig.colorbar(cs)
    cbar.ax.get_yaxis().labelpad = 25
    cbar.ax.set_ylabel('{}'.format(MOI), fontsize=15, rotation=270)
    # Grid and ticks ----------------------------------------------------------
    if xSca == 'log':
        gZeroX = [i for i in list(sorted(x.unique())) if i>0] 
        ax.set_xticks([i/scalers[0] for i in gZeroX])
        ax.axes.xaxis.set_ticklabels(gZeroX)
    else:
        ax.set_xticks([i/scalers[0] for i in list(sorted(x.unique()))])
        ax.axes.xaxis.set_ticklabels(sorted(x.unique()))
    if ySca == 'log':
        gZeroY = [i for i in list(sorted(y.unique())) if i>0] 
        ax.set_yticks([i/scalers[1] for i in gZeroY])
        ax.axes.yaxis.set_ticklabels(gZeroY)
    else:
        ax.set_yticks([i/scalers[1] for i in list(sorted(y.unique()))])
        ax.axes.yaxis.set_ticklabels(sorted(y.unique()))
    ax.grid(which='major', axis='x', lw=.1, alpha=0.3, color=(0, 0, 0))
    ax.grid(which='major', axis='y', lw=.1, alpha=0.3, color=(0, 0, 0))
    # Labels ------------------------------------------------------------------
    ax.set_xlabel(HD_IND[0])
    ax.set_ylabel(HD_IND[1])
    pTitle = ' '.join(['[{}: {}]'.format(i, fltr[i]) for i in fltr])
    plt.title(pTitle, fontsize=7.5)
    # Axes scales and limits --------------------------------------------------
    ax.set_xscale(xSca)
    ax.set_yscale(ySca)
    plt.xlim(ran[0][0], ran[0][1])
    plt.ylim(ran[1][0], ran[1][1])
    ###########################################################################
    # Export File
    ###########################################################################
    # Generate filename -------------------------------------------------------
    (allKeys, fltrKeys) = (list(aux.DATA_SCA.keys()), set(fltr.keys()))
    fElements = []
    for (i, k) in enumerate(allKeys):
        if k in fltrKeys:
            xEl = str(int(fltr[k]*aux.DATA_SCA[k])).zfill(aux.DATA_PAD[k])
        else:
            xEl = 'X'*aux.DATA_PAD[k]
        fElements.append(xEl)
    fName = '{}_{}_{}-E_'.format(
            MOI, HD_IND[0][2:], HD_IND[1][2:]
        )+'_'.join(fElements)
    # Save file ---------------------------------------------------------------
    fig.savefig(
        path.join(PT_IMG, fName+'.png'), 
        dpi=500, bbox_inches='tight', pad=0
    )
    # Clearing and closing (fig, ax) ------------------------------------------
    plt.clf()
    plt.cla() 
    plt.close(fig)
    plt.gcf()