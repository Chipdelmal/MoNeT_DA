#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import dill
import mlens
import numpy as np
from os import path
import pandas as pd
from datetime import datetime
from mlens.ensemble import SuperLearner
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import SGDRegressor
from sklearn. preprocessing import MinMaxScaler, StandardScaler
from sklearn.neural_network import MLPRegressor
from xgboost.sklearn import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split, cross_validate
import MoNeT_MGDrivE as monet
import PGS_aux as aux
import PGS_gene as drv
import PGS_mlrMethods as mth
mlens.config.set_backend('multiprocessing')

if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'PGS', '50', 'HLT', '0.1', 'CPT')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
    QNT = None if (QNT == 'None') else QNT
# Setup number of threads -----------------------------------------------------
(DATASET_SAMPLE, VERBOSE, JOB, FOLDS, SAMPLES) = (1, 0, 20, 5, 250)
CHUNKS = JOB
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
(X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size=0.5)
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
            hidden_layer_sizes=[10, 10, 10, 10],
            alpha=2.75e-3
        ),
    ],
    'sc': [
        # mth.selectMLKeras(MOI, QNT, inDims=X_train.shape[1])[-1],
        SVR(),
        LGBMRegressor(verbose=0),
        XGBRegressor(),
        MLPRegressor(
            activation='tanh',
            hidden_layer_sizes=[10, 20, 10],
            alpha=2.75e-3
        ),
        # MLPRegressor(
        #     activation='relu',
        #     hidden_layer_sizes=[10, 20, 10],
        #     alpha=2.75e-3
        # ),
    ]
}
rg = SuperLearner(
    scorer=r2_score, sample_size=SAMPLES, 
    verbose=VERBOSE, n_jobs=JOB
)
rg.add(estimators, preprocess, folds=FOLDS)
rg.add_meta(MLPRegressor(hidden_layer_sizes=[3, 3], activation='relu'))
###############################################################################
# Train
###############################################################################
rg.fit(X_train, y_train, verbose=VERBOSE, n_jobs=JOB)
y_val = rg.predict(X_test)
print(rg.data)
print('Super Learner: %.3f'%(r2_score(y_val, y_test)))
###############################################################################
# Dump to Disk
###############################################################################
fPath = path.join(PT_OUT, fNameOut)+'.pkl'
with open(fPath, "wb") as file:
    dill.dump(rg, file)
# Exporting samples -----------------------------------------------------------
samples = {
    'X_train': X_train, 'x_test': X_test, 
    'Y_train': y_train, 'y_test': y_test
}
fPath = path.join(PT_OUT, fNameOut+'_SMP')+'.pkl'
with open(fPath, 'wb') as file:
    dill.dump(samples, file)
