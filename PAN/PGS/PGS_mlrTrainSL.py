#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
# import shap
import numpy as np
from os import path
import pandas as pd
# import matplotlib.pyplot as plt
from itertools import product
from datetime import datetime
from mlens.ensemble import SuperLearner
from mlens.metrics.metrics import rmse
from mlens.visualization import pca_comp_plot, pca_plot
from sklearn.decomposition import PCA
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
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
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
REDUCE_DATASET = .15
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
df = pd.read_csv(path.join(PT_OUT, fName)).sample(frac=REDUCE_DATASET)
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
ensemble = SuperLearner(scorer=r2_score, verbose=2)
ensemble.add([SVR(), Lasso(), RandomForestRegressor()], folds=10)
ensemble.add_meta(SVR())
###############################################################################
# Train
###############################################################################
ensemble.fit(X_train, y_train, verbose=2)
y_val = ensemble.predict(X_test)
print('Super Learner: %.3f' % (r2_score(y_val, y_test)))
# pca_plot(X, PCA(n_components=2), y=y, cmap='Blues')

# import numpy as np
# from pandas import DataFrame
# from sklearn.metrics import accuracy_score
# from sklearn.datasets import load_iris

# seed = 2017
# np.random.seed(seed)

# data = load_iris()
# idx = np.random.permutation(150)
# X = data.data[idx]
# y = data.target[idx]

# from mlens.ensemble import SuperLearner
# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC

# # --- Build ---
# # Passing a scoring function will create cv scores during fitting
# # the scorer should be a simple function accepting to vectors and returning a scalar
# ensemble = SuperLearner(scorer=accuracy_score, random_state=seed)

# # Build the first layer
# ensemble.add([RandomForestClassifier(random_state=seed), LogisticRegression()])

# # Build the second layer
# ensemble.add([LogisticRegression(), SVC()])

# # Attach the final meta estimator
# ensemble.add_meta(SVC())
# ensemble.fit(X[:75], y[:75])
# preds = ensemble.predict(X[75:])
# print("Fit data:\n%r" % ensemble.data)