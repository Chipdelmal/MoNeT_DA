import sys
import random
import subprocess
from os import path
from re import match
from glob import glob
from itertools import product
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
    (USR, LND, AOI, QNT, MOI) = ('dsk', 'PAN', 'HLT', '50', 'CPT')
else:
    (USR, LND, AOI, QNT, MOI) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
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
PT_IMG = path.join(PT_OUT, 'img', 'heat')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
###############################################################################
# Select surface variables
###############################################################################
HD_IND = ['i_ren', 'i_res']
(scalers, HD_DEP, _, cmap) = aux.selectDepVars(MOI, AOI)
(ngdx, ngdy) = (1000, 1000)
(xSca, ySca) = ('linear', 'linear')
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
# (zmin, zmax) = (min(DATA[MOI])*2, max(DATA[MOI]))
(zmin, zmax) = (-0.1, max(DATA[MOI]))
# (lvls, mthd) = (np.arange(zmin*.9, zmax*1.1, (zmax-zmin)/20), 'linear')
(lvls, mthd) = (np.arange(-0.1, 1.1, 1.5/20), 'nearest')
# Filter the dataframe --------------------------------------------------------
headerInd = [i for i in DATA.columns if i[0]=='i']
uqVal = {i: list(DATA[i].unique()) for i in headerInd}
###############################################################################
# Filter dataframe
###############################################################################
fltr = {
    'i_sex': 2,
    'i_ren': 2,
    'i_res': .2,
    'i_rsg': 0,
    'i_gsv': 0,
    'i_fcf': 1.5,
    'i_mfm': 0.73,
    'i_mft': 0.93,
    'i_hrm': 0.611,
    'i_hrt': 0.916,
    'i_grp': 0, 'i_mig': 0
}
[fltr.pop(i) for i in HD_IND]
# Sweep over values -----------------------------------------------------------
kSweep = 'i_rsg'
sweep = uqVal[kSweep]
for sw in sweep:
    fltr[kSweep] = sw
    ks = [all(i) for i in zip(*[DATA[k]==fltr[k] for k in list(fltr.keys())])]
    dfSrf = DATA[ks]
    if dfSrf.shape[0] == 0:
        continue
    ###############################################################################
    # Generate Surface
    ###############################################################################
    (x, y, z) = (dfSrf[HD_IND[0]], dfSrf[HD_IND[1]], dfSrf[MOI])
    rs = monet.calcResponseSurface(
        x, y, z, 
        scalers=[max(DATA[HD_IND[0]]), max(DATA[HD_IND[1]]), 1], mthd=mthd,
        xAxis=xSca, yAxis=ySca,
        DXY=(ngdx, ngdy)
    )
    # Get ranges ------------------------------------------------------------------
    (a, b) = ((min(x), max(x)), (min(y), max(y)))
    (rsG, rsS) = (rs['grid'], rs['surface'])
    # Plot the response surface ---------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(10, 8))
    # Experiment points, contour lines, response surface
    xy = ax.plot(rsG[0], rsG[1], 'k.', ms=3, alpha=.25, marker='.')
    cc = ax.contour(rsS[0], rsS[1], rsS[2], levels=lvls, colors='w', linewidths=.5, alpha=.25)
    cs = ax.contourf(rsS[0], rsS[1], rsS[2], levels=lvls, cmap=cmap, extend='max')
    # Styling ---------------------------------------------------------------------
    cbar = fig.colorbar(cs)
    cbar.ax.get_yaxis().labelpad = 25
    cbar.ax.set_ylabel('{}'.format(MOI), fontsize=15, rotation=270)
    ax.grid(which='both', axis='y', lw=.1, alpha=0.1, color=(0, 0, 0))
    ax.grid(which='minor', axis='x', lw=.1, alpha=0.1, color=(0, 0, 0))
    ax.set_xlabel(HD_IND[0])
    ax.set_ylabel(HD_IND[1])
    ax.axes.xaxis.set_ticklabels(dfSrf[HD_IND[0]].unique())
    ax.axes.yaxis.set_ticklabels(dfSrf[HD_IND[1]].unique())
    plt.xlim(0, 1)# a[0], a[1])
    plt.ylim(0, 1)# b[0], b[1])
    pTitle = ' '.join(['[{}: {}]'.format(i, fltr[i]) for i in fltr])
    plt.title(pTitle, fontsize=7.5)
    ###############################################################################
    # Export File
    ###############################################################################
    # Generate filename -----------------------------------------------------------
    (allKeys, fltrKeys) = (list(aux.DATA_SCA.keys()), set(fltr.keys()))
    fElements = []
    for (i, k) in enumerate(allKeys):
        if k in fltrKeys:
            xEl = str(int(fltr[k]*aux.DATA_SCA[k])).zfill(aux.DATA_PAD[k])
        else:
            xEl = 'X'*aux.DATA_PAD[k]
        fElements.append(xEl)
    fName = 'E_'+'_'.join(fElements)
    # Save file -------------------------------------------------------------------
    fig.savefig(
        path.join(PT_IMG, fName+'.png'), 
        dpi=500, bbox_inches='tight', pad=0
    )
    # Clearing and closing (fig, ax) ----------------------------------------------
    plt.clf()
    plt.cla() 
    plt.close(fig)
    plt.gcf()