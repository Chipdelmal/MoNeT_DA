
import sys
import shap
from os import path
import numpy as np
import pandas as pd
from numpy import full
from functools import reduce
from datetime import datetime
import MoNeT_MGDrivE as monet
import PGS_aux as aux
import PGS_gene as drv
import matplotlib.pyplot as plt
import rfpimp as rfp
import compress_pickle as pkl
from sklearn.metrics import r2_score, explained_variance_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import ShuffleSplit
from sklearn.inspection import permutation_importance
from sklearn.inspection import plot_partial_dependence
from sklearn.inspection import PartialDependenceDisplay
# https://shap.readthedocs.io/en/latest/index.html
# https://mljar.com/blog/feature-importance-in-random-forest/
# https://www.kaggle.com/code/vikumsw/explaining-random-forest-model-with-shapely-values

if monet.isNotebook():
    (USR, DRV, AOI, THS, MOI) = ('srv', 'PGS', 'HLT', '0.1', 'WOP')
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
(X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size=0.2)
# scaler = StandardScaler().fit(X_train)
# X_trainSC = scaler.transform(X_train)
###############################################################################
# Train Model
###############################################################################
scoring = [
    'explained_variance', 'max_error',
    'neg_mean_absolute_error', 'neg_root_mean_squared_error', 'r2'
]
rf = RandomForestRegressor(
    oob_score=True, criterion='squared_error', # 'absolute_error'
    n_jobs=aux.JOB_DSK*2, verbose=False
)
cv = ShuffleSplit(n_splits=10, test_size=0.1, random_state=0)
scores = cross_validate(rf, X_train, y_train, cv=cv, scoring=scoring)
print(scores)
###############################################################################
# Train Model
###############################################################################
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
scoresFinal = {
    'r2': r2_score(y_test, y_pred),
    'explained_variance': explained_variance_score(y_test, y_pred),
    'neg_root_mean_squared_error': mean_squared_error(y_test, y_pred, squared=False),
    'neg_mean_absolute_error': mean_absolute_error(y_test, y_pred)
}
# Permutation scikit ----------------------------------------------------------
perm_importance = permutation_importance(rf, X_test, y_test)
sorted_idx = perm_importance.importances_mean.argsort()
# plt.barh(indVars[:-1], perm_importance.importances_mean)
# Importances -----------------------------------------------------------------
impRF = {k: v for (k, v) in zip(indVars[:-1], rf.feature_importances_)}
# plt.barh(indVars[:-1], rf.feature_importances_)
# Permutation RF --------------------------------------------------------------
featImportance = list(rf.feature_importances_)
impPM = rfp.permutation_importances(rf, X_train, y_train, rfp.oob_regression_r2_score)
impPMD = impPM.to_dict()['Importance']
# plt.barh(list(impPMD.keys()), list(impPMD.values()))
# SHAP ------------------------------------------------------------------------
# explainer = shap.TreeExplainer(rf)
# shap_values = explainer.shap_values(X_test, approximate=True)
# shap_obj = explainer(X_test, algorithm='permutation')
# shap.summary_plot(shap_values, X_test, plot_type="bar")
# shap.plots.beeswarm(shap_obj)
###############################################################################
# PDP/ICE Plots
###############################################################################
fNameOut = '{}_{}T_{}-MLR.png'.format(AOI, int(float(THS)*100), MOI)
display = PartialDependenceDisplay.from_estimator(
    rf, X, indVars[:-1],
    subsample=500, n_jobs=aux.JOB_DSK*2,
    n_cols=round((len(indVars)-1)/2), 
    kind='both', grid_resolution=200, random_state=0,
    ice_lines_kw={'linewidth': 0.200, 'alpha': 0.175},
    pd_line_kw={'color': '#f72585'}
)
display.figure_.subplots_adjust(hspace=.3)
for r in range(len(display.axes_)):
    for c in range(len(display.axes_[0])):
        display.axes_[r][c].set_ylabel("")
        display.axes_[r][c].get_legend().remove()
display.figure_.savefig(
    path.join(PT_IMG, fNameOut), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
###############################################################################
# Dump Model to Disk
###############################################################################
fName = fNameOut[:-3]+'pkl'
pkl.dump(rf, path.join(PT_OUT, fName))
###############################################################################
# Dump Importances to Disk
###############################################################################
iVars = [i[0] for i in aux.SA_RANGES]
permSci = pd.DataFrame({
    'names': iVars,
    'mean': perm_importance['importances_mean'], 
    'std': perm_importance['importances_std']
})
permRF = impPM.reset_index()
permSci.to_csv(path.join(PT_OUT, fNameOut[:-4]+'_PMI-SCI.csv'), index=False)
permRF.to_csv(path.join(PT_OUT, fNameOut[:-4]+'_PMI-RFI.csv'), index=False)