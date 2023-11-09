#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from os import path
import pandas as pd
from numpy.random import uniform
import matplotlib.pyplot as plt
from itertools import product
from datetime import datetime
from mlens.ensemble import SuperLearner
from mlens.metrics.metrics import rmse
from mlens.visualization import pca_comp_plot, pca_plot
from sklearn.decomposition import PCA
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.kernel_ridge import KernelRidge
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
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
(DATASET_SAMPLE, VERBOSE, JOB, FOLDS, SAMPLES) = (0.1, 0, 4, 5, 200)
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
    ],
    'sc': [
        SVR(),
        MLPRegressor(hidden_layer_sizes=[10, 20, 10]),
        LGBMRegressor(verbose=0),
        XGBRegressor(),
    ]
}
rg = SuperLearner(
    scorer=r2_score, sample_size=SAMPLES, 
    verbose=VERBOSE, n_jobs=JOB
)
rg.add(estimators, preprocess, folds=FOLDS)
rg.add_meta(MLPRegressor(hidden_layer_sizes=[5, ]))
###############################################################################
# Train
###############################################################################
rg.fit(X_train, y_train, verbose=VERBOSE, n_jobs=JOB)
y_val = rg.predict(X_test)
print(rg.data)
print('Super Learner: %.3f'%(r2_score(y_val, y_test)))
# pca_plot(X, PCA(n_components=2), y=y, cmap='Blues')
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
IVAR_IX = 2
IVAR_DELTA = .1
IVAR_STEP = 1
AUTO_RANGE = True
TRACES = 1000
MODEL = rg
YLIM = (0, 1)
TITLE = df.columns[IVAR_IX]
# Get sampling ranges for variables -------------------------------------------
if (AUTO_RANGE==True):
    minMax = [np.min(X_train, axis=0), np.max(X_train, axis=0)]
    varRanges = list(zip(*minMax))
# Get original sampling scheme (no X sweep yet) -------------------------------
samples = np.zeros((len(varRanges), TRACES))
for (ix, ran) in enumerate(varRanges):
    samples[ix] = uniform(low=ran[0], high=ran[1], size=(TRACES,))
samples = samples.T
# Get independent variable steps (x sweep) ------------------------------------
(rMin, rMax) = (varRanges[IVAR_IX][0], varRanges[IVAR_IX][1])
step = IVAR_STEP if IVAR_STEP else (rMax-rMin)*IVAR_DELTA
ivarSteps = np.arange(rMin, rMax+step, step)
# Evaluate model on steps -----------------------------------------------------
traces = np.zeros((samples.shape[0], ivarSteps.shape[0]))
for six in range(samples.shape[0]):
    smpSubset = np.tile(samples[six], [ivarSteps.shape[0], 1])
    for (r, ivar) in enumerate(ivarSteps):
        smpSubset[r][IVAR_IX] = ivar
    yOut = rg.predict(smpSubset, verbose=False)
    traces[six] = yOut
# Plot ------------------------------------------------------------------------
(fig, ax) = plt.subplots(figsize=(5, 5))
ax.plot(
    ivarSteps, traces.T, 
    color='#03045e33', lw=0.2
)
ax.plot(
    ivarSteps, np.mean(traces, axis=0),
    color='#ef476fff', ls=':', lw=3
)
# Axis and frame 
ylim = YLIM if YLIM else (np.min(traces), np.max(traces))
ax.set_xlim(ivarSteps[0], ivarSteps[-1])
ax.set_ylim(*YLIM)
if TITLE:
    ax.set_title(TITLE)

