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
    (USR, LND, AOI, DRV, QNT, MOI) = ('lab', 'PAN', 'HLT', 'LDR', '50', 'WOP')
else:
    (USR, LND, AOI, DRV, QNT, MOI) = (
        sys.argv[1], sys.argv[2], sys.argv[3], 
        sys.argv[4], sys.argv[5], sys.argv[6]
    )
TICKS_HIDE = True
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
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
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
    ['i_fch', 'i_fcb'], 'i_sex'
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
# Contour levels --------------------------------------------------------------
# Z levels
if MOI == 'TTI':
    (zmin, zmax) = (45, 90)
    (lvls, mthd) = (np.arange(zmin*1, zmax*1, (zmax-zmin)/15), 'linear')
elif MOI == 'WOP':
    (zmin, zmax) = (-5, 5*365)
    (lvls, mthd) = (np.arange(zmin*1, zmax*1, (zmax-zmin)/15), 'linear')
elif MOI == 'CPT':
    (zmin, zmax) = (0, 1.05)
    (lvls, mthd) = (np.arange(zmin*1, zmax*1, (zmax-zmin)/25), 'linear')
else:
    (zmin, zmax) = (min(DATA[MOI]), max(DATA[MOI]))
    (lvls, mthd) = (np.arange(zmin*1, zmax*1, (zmax-zmin)/15), 'linear')

if zmax > 10:
    rval = 0
else:
    rval = 3
# (zmin, zmax) = (-0.1, max(DATA[MOI]))
# (lvls, mthd) = (np.arange(-0.1, 1.1, 1.5/20), 'nearest')
# Filter the dataframe --------------------------------------------------------
headerInd = [i for i in DATA.columns if i[0]=='i']
uqVal = {i: list(DATA[i].unique()) for i in headerInd}
###############################################################################
# Filter dataframe
###############################################################################
fltr = {
    'i_sex': 1,
    'i_ren': 12,
    'i_res': .5,
    'i_rsg': 0.079,
    'i_gsv': 0.01,
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
sw = sweep[0]
for sw in sweep:
    fltr[kSweep] = sw
    ks = [all(i) for i in zip(*[np.isclose(DATA[k], fltr[k]) for k in list(fltr.keys())])]
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
    cc = ax.contour(rsS[0], rsS[1], rsS[2], levels=lvls, colors='#000000', linewidths=.5, alpha=1)
    cs = ax.contourf(rsS[0], rsS[1], rsS[2], levels=lvls, cmap=cmap, extend='max')
    # cs.cmap.set_over('red')
    # cs.cmap.set_under('white')
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
    if not TICKS_HIDE:
        ax.set_xlabel(HD_IND[0])
        ax.set_ylabel(HD_IND[1])
        pTitle = ' '.join(['[{}: {}]'.format(i, fltr[i]) for i in fltr])
        plt.title(pTitle, fontsize=7.5)
    if MOI=='WOP':
        fmt = {}
        strs = ["{:.2f}".format(i/365) for i in cc.levels]
        for (l, s) in zip(cc.levels, strs):
            fmt[l] = s
        ax.clabel(
            cc, cc.levels[1::2], inline=True, fontsize=20, fmt=fmt,
            rightside_up=False, inline_spacing=5
        )
    else:
        ax.clabel(
            cc, inline=True, fontsize=20, fmt='%1.{}f'.format(rval),
            rightside_up=True
        )
    # Axes scales and limits --------------------------------------------------
    ax.set_xscale(xSca)
    ax.set_yscale(ySca)
    renB = (HD_IND[0]=='i_ren') or (HD_IND[1]=='i_ren')
    resB = (HD_IND[0]=='i_res') or (HD_IND[1]=='i_res')
    if renB and resB:
        ax.xaxis.set_ticks(np.arange(0, 24, 4))
        ax.yaxis.set_ticks(np.arange(0, 1, 0.2))
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


DATA[
    (DATA['i_ren']==12) &
    (DATA['i_res']==0.5)
]