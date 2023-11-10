#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from os import path
import pandas as pd
from numpy.random import uniform
import matplotlib.pyplot as plt
from datetime import datetime
from mlens.ensemble import SuperLearner
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import SGDRegressor
from sklearn. preprocessing import MinMaxScaler, StandardScaler
from sklearn.neural_network import MLPRegressor
from xgboost.sklearn import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score, explained_variance_score
from sklearn.metrics import d2_absolute_error_score, median_absolute_error
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import make_scorer
from sklearn.inspection import permutation_importance
from sklearn.inspection import PartialDependenceDisplay
import MoNeT_MGDrivE as monet
import PGS_aux as aux
import PGS_gene as drv
# import PGS_mlrMethods as mth

if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('sami', 'PGS', '50', 'HLT', '0.1', 'CPT')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
(DATASET_SAMPLE, VERBOSE, JOB, FOLDS, SAMPLES) = (1, 0, 4, 5, 200)
CHUNKS = JOB
C_VAL = True
DEV = True
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
    '{} mlrTrainMLQNT [{}:{}:{}:{}]'.format(DRV, AOI, QNT, THS, MOI)
)
###############################################################################
# Read Dataframe
###############################################################################
if QNT:
    fName = 'SCA_{}_{}Q_{}T.csv'.format(AOI, int(QNT), int(float(THS)*100))
else:
    fName = 'SCA_{}_{}T_MLR.csv'.format(AOI, int(float(THS)*100))
df = pd.read_csv(path.join(PT_OUT, fName)).sample(frac=DATASET_SAMPLE)
###############################################################################
# Split I/O
###############################################################################
indVars = [i[0] for i in aux.DATA_HEAD]
indVarsLabel = [i[2:] for i in indVars][:-1]
dfIn = df[indVars].drop('i_grp', axis=1)
(X, y) = [np.array(i) for i in (dfIn, df[MOI])]
if MOI=='WOP':
    y = y/aux.XRAN[1]
elif MOI=='CPT':
    y = 1-y
(X_trainR, X_testR, y_train, y_test) = train_test_split(X, y, test_size=0.25)
(X_train, X_test) = (X_trainR, X_testR)
inDims = X_train.shape[1]
###############################################################################
# Setup Model
###############################################################################
preprocess = {'mm': [MinMaxScaler()], 'sc': [StandardScaler()]}
estimators = {
    'mm': [
        SGDRegressor(), 
        BayesianRidge(),
        MLPRegressor(
            activation='tanh',
            hidden_layer_sizes=[10, 10, 10, 10]
        ),
    ],
    'sc': [
        SVR(),
        LGBMRegressor(verbose=0),
        XGBRegressor(),
        MLPRegressor(
            activation='tanh',
            hidden_layer_sizes=[10, 20, 10]
        ),
        MLPRegressor(
            activation='relu',
            hidden_layer_sizes=[10, 20, 10]
        ),
    ]
}
rg = SuperLearner(
    scorer=r2_score, sample_size=SAMPLES, 
    verbose=VERBOSE, n_jobs=JOB
)
rg.add(estimators, preprocess, folds=FOLDS)
rg.add_meta(MLPRegressor(hidden_layer_sizes=[5, ], activation='tanh'))
###############################################################################
# Train
###############################################################################
rg.fit(X_train, y_train, verbose=VERBOSE, n_jobs=JOB)
y_val = rg.predict(X_test)
print(rg.data)
print('Super Learner: %.3f'%(r2_score(y_val, y_test)))
###############################################################################
# Permutation Importance
###############################################################################
(X_trainS, y_trainS) = aux.unison_shuffled_copies(
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
clr = aux.selectColor(MOI)
(fig, ax) = plt.subplots(figsize=(4, 6))
plt.barh(indVars[:-1][::-1], pImp[::-1], color=clr, alpha=0.8)
ax.set_xlim(0, 1)
###############################################################################
# PDP/ICE Dev
###############################################################################
(MODEL_PREDICT, IVAR_IX) = (rg.predict, 1)
(IVAR_DELTA, IVAR_STEP) = (.01, 1)
(TRACES, YLIM) = (3000, (0, 1))
TITLE = df.columns[IVAR_IX]
# Get sampling ranges for variables -------------------------------------------
pdpice = monet.getSamples_PDPICE(
    MODEL_PREDICT, IVAR_IX, tracesNum=TRACES,
    X=X_train, varRanges=None, indVarStep=IVAR_STEP
)
# Plot ------------------------------------------------------------------------
(fig, ax) = plt.subplots(figsize=(5, 5))
(fig, ax) = monet.plotPDPICE(
    pdpice, (fig, ax), YLIM=YLIM, TITLE=TITLE,
    pdpKwargs={'color': '#023e8a33', 'ls': '-', 'lw': 0.125},
    iceKwargs={'color': '#E84E73ff', 'ls': ':', 'lw': 3}
)
ax.grid(color='#bfc0c0ff', linestyle = '--', linewidth = 0.5)