#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import dill
import mlens
import numpy as np
from os import path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.metrics import make_scorer
from sklearn.metrics import mean_squared_error
from sklearn.inspection import permutation_importance
import MoNeT_MGDrivE as monet
import TPP_aux as aux
import TPP_gene as drv
import TPP_mlrMethods as mth
mlens.config.set_backend('multiprocessing')

if monet.isNotebook():
    (USR, LND, EXP, DRV, AOI, QNT, THS, MOI) = (
        'zelda', 
        'Kenya', 'highEIR', 
        'HUM', 'CSS', '50', '0.1', 'CPT'
    )
else:
    (USR, LND, EXP, DRV, AOI, QNT, THS, TRC) = sys.argv[1:]
    QNT = None if (QNT == 'None') else QNT
# Setup number of threads -----------------------------------------------------
(DATASET_SAMPLE, VERBOSE, JOB, FOLDS, SAMPLES) = (1, 0, 20, 2, 1000)
CHUNKS = JOB
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
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_OUT, tS, 
    '{} mlrTrainMLQNT [{}:{}:{}:{}]'.format(DRV, AOI, QNT, THS, MOI)
)
# Output name -----------------------------------------------------------------
modID = 'slr'
if QNT:
    fNameOut = '{}_{}Q_{}T_{}-{}-MLR'.format(
        AOI, int(QNT), int(float(THS)*100), MOI, modID
    )
else:
    fNameOut = '{}_{}T_{}-{}-MLR'.format(AOI, int(float(THS)*100), MOI, modID)
###############################################################################
# Read Dataframe
###############################################################################
if QNT:
    fName = 'SCA_{}_{}Q_{}T.csv'.format(AOI, int(QNT), int(float(THS)*100))
else:
    fName = 'SCA_{}_{}T_MLR.csv'.format(AOI, int(float(THS)*100))
df = pd.read_csv(path.join(PT_OUT, fName)).sample(frac=DATASET_SAMPLE)
(X, y) = [np.array(i) for i in (df, df[MOI])]
###############################################################################
# Load Files
###############################################################################
fPath = path.join(PT_OUT, fNameOut)+'.pkl'
with open(fPath, 'rb') as dill_file:
    rg = dill.load(dill_file)
# Exporting samples -----------------------------------------------------------
fPath = path.join(PT_OUT, fNameOut+'_SMP')+'.pkl'
with open(fPath, 'rb') as dill_file:
    samples = dill.load(dill_file)
(X_train, X_test, y_train, y_test) = (
    samples['X_train'], samples['x_test'],
    samples['Y_train'], samples['y_test']
)
indVars = [i[0] for i in aux.DATA_HEAD]
indVarsLabel = [i[2:] for i in indVars][:-1]
###############################################################################
# Permutation Importance
###############################################################################
(X_trainS, y_trainS) = mth.unison_shuffled_copies(
    X_train, y_train, size=int(5e3)
)
# Permutation scikit ----------------------------------------------------------
perm_importance = permutation_importance(
    rg, X_trainS, y_trainS, 
    scoring=make_scorer(mean_squared_error)
)
sorted_idx = perm_importance.importances_mean.argsort()
pImp = perm_importance.importances_mean/sum(perm_importance.importances_mean)
labZip = zip(perm_importance.importances_mean, indVars[:-1])
labSort = [x for _, x in sorted(labZip)]
# Perm figure -----------------------------------------------------------------
fPath = './tmp/'+fNameOut+f'_PERM.png'
clr = aux.selectColor(MOI)
(fig, ax) = plt.subplots(figsize=(4, 6))
plt.barh(indVars[:-1][::-1], pImp[::-1], color=clr, alpha=0.8)
ax.set_xlim(0, 1)
plt.savefig(
    path.join(fPath), 
    dpi=200, bbox_inches='tight', pad_inches=0, transparent=True
)
plt.close()
###############################################################################
# PDP/ICE Dev
###############################################################################
(IVAR_DELTA, IVAR_STEP) = (0.1, 0.05)
(TRACES, YLIM) = (500, (0, 1))
VRANS = mth.getRanges(df, ['i_shc', 'i_sbc', 'i_hdr', 'i_rgr', 'i_inf'])
for ix in list(range(X_train.shape[-1])):
    (MODEL_PREDICT, IVAR_IX) = (rg.predict, ix)
    TITLE = df.columns[IVAR_IX]
    # IVAR_STEP = 1 if (np.max(X.T[IVAR_IX]) > 1) else 0.1
    # Get sampling ranges for variables ---------------------------------------
    pdpice = monet.getSamples_PDPICE(
        MODEL_PREDICT, IVAR_IX, X=X_train, 
        tracesNum=TRACES, varRanges=VRANS, 
        indVarDelta=None, indVarStep=IVAR_STEP
    )
    # Plot --------------------------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(5, 5))
    (fig, ax) = monet.plotPDPICE(
        pdpice, (fig, ax), YLIM=YLIM, TITLE=TITLE,
        pdpKwargs={'color': '#5465ff20', 'ls': '-', 'lw': 0.1},
        iceKwargs={'color': '#E84E73ff', 'ls': ':', 'lw': 3}
    )
    ax.grid(color='#bfc0c0ff', linestyle='--', linewidth=0.5)
    ax.set_xlim(VRANS[ix][0], VRANS[ix][1])
    fPath = path.join(PT_OUT, fNameOut)+f'_{TITLE[2:]}'
    fPath = './tmp/'+fNameOut+f'_{TITLE[2:]}.png'
    print(fPath)
    plt.savefig(
        fPath, 
        dpi=500, bbox_inches='tight', 
        pad_inches=0.1, transparent=False
    )
    # plt.close()
