
import sys
import numpy as np
from os import path
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
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
poeDFRaw = dfFltr[dfFltr['POE']>=0.9]
poeDF = poeDFRaw.drop(labels=cats, axis=1).drop(labels=outs, axis=1)
###############################################################################
# Explore ranges
###############################################################################
poeDF['mfr+fvb'] = poeDF['i_mfr']+poeDF['i_fvb']
poeDF['ren*res'] = poeDF['i_ren']*poeDF['i_res']
# Explore ---------------------------------------------------------------------
min(poeDF['i_ren'].unique())
min(poeDF['i_res'].unique())
sorted(poeDF['i_mfr'].unique())
sorted(poeDF['i_fvb'].unique())
poeDF[poeDF['mfr+fvb']>=0.4]
###############################################################################
# Cluster
###############################################################################
y_pred = KMeans(n_clusters=4).fit_predict(poeDF)
poeDF['KMeans'] = y_pred