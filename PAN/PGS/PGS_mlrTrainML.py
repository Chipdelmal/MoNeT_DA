
import sys
from os import path
import numpy as np
from numpy import full
import pandas as pd
from functools import reduce
from datetime import datetime
import MoNeT_MGDrivE as monet
import PGS_aux as aux
import PGS_gene as drv
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.linear_model import QuantileRegressor, LinearRegression
from sklearn.linear_model import SGDRegressor, LassoLars, BayesianRidge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import ShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import plot_partial_dependence

if monet.isNotebook():
    (USR, DRV, AOI, THS, MOI) = ('srv', 'PGS', 'HLT', '0.1', 'CPT')
else:
    (USR, DRV, AOI, THS, MOI) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
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
    '{} mlrTrainML [{}:{}]'.format(DRV, AOI, THS)
)
###############################################################################
# Read Dataframe
###############################################################################
fName = 'SCA_{}_{}T_MLR.csv'.format(AOI, int(float(THS)*100))
df = pd.read_csv(path.join(PT_OUT, fName))
###############################################################################
# Split I/O
###############################################################################
indVars = [i[0] for i in aux.DATA_HEAD]
dfIn = df[indVars].drop('i_grp', axis=1)
(X, y) = (dfIn, df[MOI])
(X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size=0.3)
# scaler = StandardScaler().fit(X_train)
# X_trainSC = scaler.transform(X_train)
###############################################################################
# Train Model
###############################################################################
scoring = ['neg_mean_absolute_error', 'neg_root_mean_squared_error', 'r2']
mlRegression = RandomForestRegressor(
    oob_score=True,
    n_jobs=aux.JOB_DSK*2, verbose=False
)
cv = ShuffleSplit(n_splits=5, test_size=0.25, random_state=0)
scores = cross_validate(
    mlRegression, X_train, y_train, cv=cv, scoring=scoring
)
print(scores)
###############################################################################
# Train and Plot ICE
###############################################################################
mlRegression.fit(X_train, y_train)
# (fig, ax) = plt.subplots(figsize=(20, 10))
display = plot_partial_dependence(
    mlRegression, X, indVars[:-1],
    kind="individual",
    subsample=500, n_jobs=aux.JOB_DSK*2,
    n_cols=round((len(indVars)-1)/2), 
    ice_lines_kw={'linewidth': 0.200, 'alpha': 0.175},
    grid_resolution=20, random_state=0,
)
display.figure_.subplots_adjust(hspace=.5)