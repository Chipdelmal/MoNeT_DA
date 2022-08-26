

import math
from os import sys
from os import path
import numpy as np
import pandas as pd
import compress_pickle as pkl
from SALib.analyze import rbd_fast, delta, pawn, hdmr
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import squarify
import FMS_aux as aux
import FMS_gene as drv


if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'PGS', '50', 'HLT', '0.1', 'CPT')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
###############################################################################
# Setting Paths Up and Reading SA Constants
###############################################################################
(SAMPLES_NUM, VARS_RANGES) = (aux.SA_SAMPLES, aux.SA_RANGES)
(drive, land) = (
    drv.driveSelector(DRV, 'HLT', popSize=aux.POP_SIZE), 
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, fldr)
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
###############################################################################
# Read SA Files
###############################################################################
(PROBLEM, SAMPLER, EXP) = (
    pkl.load(path.join(PT_MTR, 'SA_experiment.pkl')),
    np.load(path.join(PT_MTR, 'SA_experiment.npy')),
    pd.read_csv (path.join(PT_MTR, 'SA_experiment.csv'))
)
###############################################################################
# Read Results CSV
###############################################################################
thsStr = str(int(float(THS)*100))
(fName_I, fName_R, fName_C) = (
    'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'REG_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'CLS_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr)
)
RES = pd.read_csv(path.join(PT_OUT, fName_I))
###############################################################################
# Explore
###############################################################################
headerInd = list(RES.columns)
uqVal = {i: len(list(RES[i].unique())) for i in headerInd}
RES.shape
###############################################################################
# Assemble Output Vector
###############################################################################
(FEATS, LABLS) = (
    [i for i in headerInd if i[0]=='i'], 
    [i for i in headerInd if i[0]!='i']
)
FEATS = [i for i in FEATS if uqVal[i]>1]
bounds = [(min(RES[i]), max(RES[i])) for i in FEATS]
problem = {
    'num_vars': len(FEATS),
    'names': FEATS,
    'bounds': bounds,
    'dists': ['unif']*len(FEATS),
    'sample_scaled': True
}
(X, Y) = (np.asarray(RES[FEATS]), np.asarray(RES[MOI]))
###############################################################################
# Run SA
###############################################################################
SA_delta = delta.analyze(problem, X, Y, print_to_console=True)
SA_pawn = pawn.analyze(problem, X, Y, print_to_console=True)
SA_hdmr = hdmr.analyze(problem, X, Y, print_to_console=True)
SA_fast = rbd_fast.analyze(problem, X, Y, print_to_console=True)
# Compile dataframes ----------------------------------------------------------
deltaDF = pd.DataFrame(SA_delta)
pawnDF = pd.DataFrame(SA_pawn)
hdmrDF = pd.DataFrame({'S1': SA_hdmr['ST'], 'names': SA_hdmr['names']})
fastDF = pd.DataFrame(SA_fast)
###############################################################################
# Plots
###############################################################################
# plt.show(SA_pawn.plot())
colors = [
    '#2614ed55', '#FF006E55', '#45d40c55', '#8338EC55', '#1888e355', 
    '#BC109755', '#FFE93E55', '#3b479d55', '#540d6e55', '#7bdff255'
]
saRes = hdmrDF
fltr = [not (math.isnan(i)) for i in saRes['S1']]
(sizes, label) = (abs(saRes['S1'][fltr]), saRes['names'][fltr])
(fig, ax) = plt.subplots(figsize=(5,5))
squarify.plot(sizes=sizes, label=label, alpha=0.5, color=colors)
ax.set_aspect(1)
plt.axis('off')
plt.show()