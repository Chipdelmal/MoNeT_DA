#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import shap
import numpy as np
from os import path
import pandas as pd
import compress_pickle as pkl
import matplotlib.pyplot as plt
from datetime import datetime
from keras.layers import Dense
from keras.models import Sequential
from keras.callbacks import EarlyStopping
from keras.regularizers import L1L2
from sklearn.metrics import r2_score, explained_variance_score
from sklearn.metrics import d2_absolute_error_score, median_absolute_error
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.inspection import permutation_importance
from scikeras.wrappers import KerasRegressor
from sklearn.inspection import PartialDependenceDisplay
import MoNeT_MGDrivE as monet
import PGS_aux as aux
import PGS_gene as drv
import PGS_mlrMethods as mth


if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'PGS', '50', 'HLT', '0.1', 'CPT')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
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
    '{} mlrTrainMLQNT [{}:{}:{}:{}]'.format(DRV, AOI, QNT, THS, MOI)
)
###############################################################################
# Read Dataframe
###############################################################################
if QNT:
    fName = 'SCA_{}_{}Q_{}T.csv'.format(AOI, int(QNT), int(float(THS)*100))
else:
    fName = 'SCA_{}_{}T_MLR.csv'.format(AOI, int(float(THS)*100))
df = pd.read_csv(path.join(PT_OUT, fName))
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
###############################################################################
# Select Model and Scores
###############################################################################
(K_SPLITS, T_SIZE) = (10, .25)
scoring = [
    'explained_variance', 'max_error',
    'neg_mean_absolute_error', 'neg_root_mean_squared_error', 'r2'
]
###############################################################################
# Define Model
###############################################################################
def build_model():
    rf = Sequential()
    rf.add(Dense(
        15, activation= "relu",
        input_dim=X_train.shape[1],
        # kernel_regularizer=L1L2(l1=1e-5, l2=0.008)
    ))
    rf.add(Dense(
        15, activation= "relu",
        # kernel_regularizer=L1L2(l1=1e-5, l2=0.008)
    ))
    rf.add(Dense(
        15, activation= "sigmoid",
        # kernel_regularizer=L1L2(l1=1e-5, l2=0.008)
    ))
    rf.add(Dense(
        1, activation='sigmoid'
    ))
    rf.compile(
        loss= "mean_squared_error" , 
        optimizer="adam", 
        metrics=["mean_squared_error"]
    )
    return rf
# Output name -----------------------------------------------------------------
modID = 'krs'
if QNT:
    fNameOut = '{}_{}Q_{}T_{}-{}-MLR'.format(
        AOI, int(QNT), int(float(THS)*100), MOI, modID
    )
else:
    fNameOut = '{}_{}T_{}-{}-MLR'.format(AOI, int(float(THS)*100), MOI, modID)
###############################################################################
# Train Model
###############################################################################
epochs=100
rf = KerasRegressor(build_fn=build_model)
rf.fit(
    X_train, y_train,
    # batch_size=250,
    epochs=epochs, validation_split=0.2,
    callbacks=EarlyStopping(
        monitor='val_loss', 
        restore_best_weights=True,
        patience=int(epochs*.1),
        verbose=1
    ),
    verbose=1
)
# Score -----------------------------------------------------------------------
y_pred = rf.predict(X_test)
scoresFinal = {
    'r2': r2_score(y_test, y_pred),
    'explained_variance': explained_variance_score(y_test, y_pred),
    'root_mean_squared_error': mean_squared_error(y_test, y_pred, squared=False),
    'mean_absolute_error': mean_absolute_error(y_test, y_pred),
    'median_absolute_error ': median_absolute_error(y_test, y_pred),
    'd2_absolute_error_score': d2_absolute_error_score(y_test, y_pred)
}
scoresFinal['r2Adj'] = aux.adjRSquared(
    scoresFinal['r2'], y_pred.shape[0], X_train.shape[1]
)
print(scoresFinal)
# Cross-validate --------------------------------------------------------------
cv = ShuffleSplit(n_splits=K_SPLITS, test_size=T_SIZE)
scores = cross_validate(
    rf, X_train, y_train, cv=cv, scoring=scoring, n_jobs=K_SPLITS
)
###############################################################################
# Permutation Importance
###############################################################################
(X_trainS, y_trainS) = aux.unison_shuffled_copies(
    X_train, y_train, size=int(5e3)
)
# Permutation scikit ----------------------------------------------------------
perm_importance = permutation_importance(
    rf, X_trainS, y_trainS, 
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
plt.savefig(
    path.join(PT_IMG, fNameOut+'_PERM.png'), 
    dpi=200, bbox_inches='tight', pad_inches=0, transparent=True
)
###############################################################################
# SHAP Importance
###############################################################################
(X_trainS, y_trainS) = aux.unison_shuffled_copies(X_train, y_train, size=200)
explainer = shap.KernelExplainer(rf.predict, X_trainS)
shap_values = explainer.shap_values(X_trainS, approximate=True)
shapVals = np.abs(shap_values).mean(0)
sImp = shapVals/sum(shapVals)
# SHAP figure -----------------------------------------------------------------
clr = aux.selectColor(MOI)
(fig, ax) = plt.subplots(figsize=(4, 6))
plt.barh(indVars[:-1][::-1], sImp[::-1], color=clr, alpha=0.8)
ax.set_xlim(0, 1)
plt.savefig(
    path.join(PT_IMG, fNameOut+'_SHAP.png'), 
    dpi=200, bbox_inches='tight', pad_inches=0, transparent=False
)
(fig, ax) = plt.subplots(figsize=(4, 6))
shap.summary_plot(
    shap_values, X_trainS,
    alpha=0.25, feature_names=indVars,
    show=False
)
plt.savefig(
    path.join(PT_IMG, fNameOut+'_SMRY.png'), 
    dpi=200, bbox_inches='tight', pad_inches=0, transparent=False
)
# shap.dependence_plot(
#     indVars.index('i_pmd'), 
#     shap_values, X_trainS, 
#     alpha=0.5, dot_size=10,
#     feature_names=indVars,
#     interaction_index=indVars.index('i_fvb')
# )
###############################################################################
# PDP/ICE Plots
###############################################################################
SAMP_NUM = 5000
clr = aux.selectColor(MOI)
X_plots = np.copy(X_train)
np.random.shuffle(X_plots)
(fig, ax) = plt.subplots(figsize=(16, 2))
rf.dummy_ = None
display = PartialDependenceDisplay.from_estimator(
    rf, X_plots[:SAMP_NUM], list(range(X_plots.shape[1])), 
    ax=ax, kind='both', subsample=SAMP_NUM,
    n_cols=round((len(indVars)-1)), 
    grid_resolution=200, random_state=0,
    ice_lines_kw={'linewidth': 0.1, 'alpha': 0.075, 'color': clr},
    pd_line_kw={'color': '#f72585'}
)
display.figure_.subplots_adjust(hspace=0.4)
ix = -1
for r in range(len(display.axes_)):
    for c in range(len(display.axes_[r])):
        try:
            ix = ix+1
            display.axes_[r][c].autoscale(enable=True, axis='x', tight=True)
            if MOI=='CPT':
                display.axes_[r][c].set_ylim(0, 1)
            else:
                display.axes_[r][c].set_ylim(0, 1)
            display.axes_[r][c].set_xlabel(indVarsLabel[ix])
            display.axes_[r][c].set_ylabel("")
            display.axes_[r][c].get_legend().remove()
        except:
            continue
display.figure_.savefig(
    path.join(PT_IMG, fNameOut+'.png'), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
###############################################################################
# Dump Model to Disk
###############################################################################
pkl.dump(rf, path.join(PT_OUT, fNameOut+'.pkl'))
pd.DataFrame(scores).to_csv(path.join(PT_OUT, fNameOut+'_CV.csv'))
pd.DataFrame(scoresFinal, index=[0]).to_csv(path.join(PT_OUT, fNameOut+'_VL.csv'))
###############################################################################
# Dump Importances to Disk
###############################################################################
iVars = [i[0] for i in aux.SA_RANGES]
permSci = pd.DataFrame({
    'names': iVars,
    'mean': perm_importance['importances_mean'], 
    'std': perm_importance['importances_std']
})
shapImp = pd.DataFrame({'names': iVars, 'mean': shapVals})
permSci.to_csv(path.join(PT_OUT, fNameOut+'_PMI-SCI.csv'), index=False)
shapImp.to_csv(path.join(PT_OUT, fNameOut+'_SHP-SHP.csv'), index=False)
