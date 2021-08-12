import sys
from os import path
from re import match
from glob import glob
from joblib import dump, load
from datetime import datetime
import numpy as np
from numpy.lib.arraypad import pad
import pandas as pd
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import colors
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
import seaborn as sns
from more_itertools import locate
from functools import reduce
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

if monet.isNotebook():
    (USR, LND, AOI, DRV, QNT) = ('dsk', 'PAN', 'HLT', 'LDR', '50')
else:
    (USR, LND, AOI, DRV, QNT) = (
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
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND, DRV)
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
###############################################################################
# Filtering to male releases only
###############################################################################
male = DATA[DATA['i_sex']==1].drop('i_sex', axis=1)
(sexLim, renLim, resLim) = (1, 50, 1.5)
# Goals constraints -----------------------------------------------------------
cptLim = (-0.1, 1.1)
poeLim = (-.1, 1)
ttiLim = (-1, 4*365)
ttoLim = (-1, 6*365)
wopLim = (0, 10*365)
mnfLim = (0, 1)
# Filter and return dataframe -------------------------------------------------
fltr = {
    'i_sex': 1, 'i_ren': 8, 
    'i_rsg': 0.079, 'i_gsv': 0.01,
    'i_fch': 0.175, 'i_fcb': 0.117, 'i_fcr': 0,
    'i_hrm': 1.0, 'i_hrf': 0.956, 
    'i_grp': 0, 'i_mig': 0
}
fltr.pop('i_ren')
keys = list(fltr.keys())
ks = [all(i) for i in zip(*[np.isclose(DATA[k], fltr[k]) for k in keys])]
resVals = list(DATA[ks]['i_res'].unique())
###############################################################################
# Plot
###############################################################################
c = mcolors.ColorConverter().to_rgb
clrs = [c(i) for i in ['#ef233c', '#9bf6ff', '#4361ee', '#3a0ca3']]
rvb = mcolors.LinearSegmentedColormap.from_list("", clrs)
colors = rvb(np.linspace(0, 1, len(resVals)))
(fig, ax) = plt.subplots(figsize=(10, 10))
fltr['i_res'] = 0.25
for (i, res) in enumerate(resVals):
    fltr['i_res'] = res
    keys = list(fltr.keys())
    ks = [all(i) for i in zip(*[np.isclose(DATA[k], fltr[k]) for k in keys])]
    dfSrf = DATA[ks]
    # plt.scatter(dfSrf['i_ren'], dfSrf['WOP'])
    plt.plot(
        list(dfSrf['i_ren']), 
        list(dfSrf['WOP']), 
        color=colors[i]
    )
ax.set_xlim(0, 24)
ax.set_ylim(0, 1.75*365)
plt.tight_layout()
fig.savefig(    
    path.join(PT_IMG, 'REN-RES_traces.png'), 
    dpi=500, bbox_inches='tight', pad=0
)