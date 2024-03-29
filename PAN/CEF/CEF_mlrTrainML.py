
import sys
import shap
from os import path
import numpy as np
import pandas as pd
import compress_pickle as pkl
from datetime import datetime
import rfpimp as rfp
from math import ceil
import matplotlib.pyplot as plt
from xgboost import XGBRFRegressor
from sklearn.metrics import r2_score, explained_variance_score
from sklearn.metrics import d2_absolute_error_score, median_absolute_error
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, ShuffleSplit
from sklearn.inspection import permutation_importance
from sklearn.inspection import PartialDependenceDisplay
import MoNeT_MGDrivE as monet
import CEF_aux as aux
import CEF_gene as drv
# https://shap.readthedocs.io/en/latest/index.html
# https://mljar.com/blog/feature-importance-in-random-forest/
# https://www.kaggle.com/code/vikumsw/explaining-random-forest-model-with-shapely-values

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
(X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size=0.2)
# scaler = StandardScaler().fit(X_train)
# X_trainSC = scaler.transform(X_train)
###############################################################################
# Train Model
###############################################################################
(MOD_SEL, K_SPLITS, T_SIZE) = ('rf', 10, .1)
scoring = [
    'explained_variance', 'max_error',
    'neg_mean_absolute_error', 'neg_root_mean_squared_error', 'r2'
]
# Select the type of regressor ------------------------------------------------
if MOD_SEL=='rf':
    modID = ''
    rf = RandomForestRegressor(
        n_estimators=100, max_depth=None, max_features="sqrt",
        oob_score=True, criterion='squared_error',
        n_jobs=aux.JOB_DSK*2, 
        verbose=False
    )
    param_grid = [{
        'n_estimators': [50, 100], 
        'max_depth':    ['20', '50', None]
    }]
    clf = GridSearchCV(
        estimator=rf, param_grid=param_grid,
        n_jobs=20
    )
elif MOD_SEL=='ada':
    rf = AdaBoostRegressor(
        DecisionTreeRegressor(max_depth=50), 
        loss='linear', n_estimators=100
    )
elif MOD_SEL=='gb':
    rf = GradientBoostingRegressor(
        n_estimators=100, max_leaf_nodes=75, max_depth=30, 
        verbose=True
    )
elif MOD_SEL=='hgb':
    modID = 'hgb'
    if MOI=='CPT':
        mono = aux.SA_MONOTONIC_CPT
    else:
        mono = aux.SA_MONOTONIC_WOP
    rf = HistGradientBoostingRegressor(
        loss='quantile', quantile=.25, 
        max_iter=1000, max_leaf_nodes=75, max_depth=None, 
        max_bins=255,
        monotonic_cst=list(mono.values()),
        verbose=True
    )
if MOD_SEL=='rfg':
    rf_o = RandomForestRegressor(
        oob_score=True, criterion='squared_error',
        n_jobs=aux.JOB_DSK*2, 
        verbose=False
    )
    param_grid = [{
        'n_estimators': [50, 100, 200], 
        'max_depth':    [20, 25, 30, 50, None],
        'max_features': ['sqrt', 'log2', None]
    }]
    rf = GridSearchCV(
        estimator=rf_o, param_grid=param_grid,
        n_jobs=8, verbose=2
    )
elif MOD_SEL=='gbg':
    rf_o = GradientBoostingRegressor()
    param_grid = [{
        'n_estimators':     [50, 100, 200], 
        'max_leaf_nodes':   [20, 30, 50, 75, None],
        'max_depth':        [20, 30, None]
    }]
    rf = GridSearchCV(
        estimator=rf_o, param_grid=param_grid,
        n_jobs=8, verbose=2
    )
elif MOD_SEL=='xgb':
    if MOI=='CPT':
        mono = aux.SA_MONOTONIC_CPT
    else:
        mono = aux.SA_MONOTONIC_WOP
    rf = XGBRFRegressor(
        n_jobs=aux.JOB_DSK*2,
        n_estimators=500, max_depth=None,
        tree_method='hist',
        max_bin=5000,
        objective='reg:squarederror',
        eval_metric='mae',
        verbose=2
    )
elif MOD_SEL=='mlp':
    modID = 'mlp-'
    rf = MLPRegressor(
        hidden_layer_sizes=(100, 50), 
        verbose=True
    )
# Cross-validate --------------------------------------------------------------
cv = ShuffleSplit(n_splits=K_SPLITS, test_size=T_SIZE)
scores = cross_validate(
    rf, X_train, y_train, cv=cv, scoring=scoring, n_jobs=K_SPLITS
)
###############################################################################
# Train Model
###############################################################################
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
scoresFinal = {
    'root_mean_squared_error': mean_squared_error(y_test, y_pred, squared=False),
    'mean_absolute_error': mean_absolute_error(y_test, y_pred),
    'median_absolute_error ': median_absolute_error(y_test, y_pred),
    'explained_variance': explained_variance_score(y_test, y_pred),
    'r2': r2_score(y_test, y_pred),
    'd2_absolute_error_score': d2_absolute_error_score(y_test, y_pred)
}
scoresFinal['r2Adj'] = aux.adjRSquared(
    scoresFinal['r2'], y_pred.shape[0], X_train.shape[1]
)
print(scoresFinal)
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
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test, approximate=True)
shapVals = np.abs(shap_values).mean(0)
# shap_obj = explainer(X_test, algorithm='permutation')
# shap.summary_plot(shap_values, X_test, plot_type="bar")
# shap.plots.beeswarm(shap_obj)
###############################################################################
# PDP/ICE Plots
###############################################################################
clr = '#3a86ff' if MOI=='CPT' else '#03045e' 
fNameOut = '{}_{}T_{}-{}MLR.png'.format(AOI, int(float(THS)*100), MOI, modID)
(fig, ax) = plt.subplots(figsize=(16, 2))
display = PartialDependenceDisplay.from_estimator(
    rf, X, indVars[:-1], ax=ax,
    subsample=1500, n_jobs=aux.JOB_DSK*2,
    n_cols=round((len(indVars)-1)), 
    kind='both', grid_resolution=200, random_state=0,
    ice_lines_kw={'linewidth': 0.1, 'alpha': 0.1, 'color': clr},
    pd_line_kw={'color': '#f72585'}
)
display.figure_.subplots_adjust(hspace=.3)
for r in range(len(display.axes_)):
    for c in range(len(display.axes_[r])):
        try:
            display.axes_[r][c].autoscale(enable=True, axis='x', tight=True)
            if MOI=='CPT':
                display.axes_[r][c].set_ylim(0, 1)
            else:
                display.axes_[r][c].set_ylim(0, aux.XRAN[1])
            display.axes_[r][c].set_xlabel("")
            display.axes_[r][c].set_ylabel("")
            display.axes_[r][c].get_legend().remove()
        except:
            continue
display.figure_.savefig(
    path.join(PT_IMG, fNameOut), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
###############################################################################
# Interaction
###############################################################################
display = PartialDependenceDisplay.from_estimator(
    rf, X, features=[['i_pct', 'i_pmd']], 
    subsample=2000, n_jobs=aux.JOB_DSK*4,
    n_cols=ceil((len(indVars)-1)), 
    kind='average', grid_resolution=200, random_state=0,
    ice_lines_kw={'linewidth': 0.1, 'alpha': 0.1},
    pd_line_kw={'color': '#f72585'}
)
###############################################################################
# Dump Model to Disk
###############################################################################
fNameOut = '{}_{}T_{}-MLR.png'.format(AOI, int(float(THS)*100), MOI)
fName = fNameOut[:-3]+'pkl'
pkl.dump(rf, path.join(PT_OUT, fName))
pd.DataFrame(scores).to_csv(path.join(PT_OUT, fName[:-4]+'_CV.csv'))
pd.DataFrame(scoresFinal, index=[0]).to_csv(path.join(PT_OUT, fName[:-4]+'_VL.csv'))
###############################################################################
# Dump Importances to Disk
###############################################################################
iVars = [i[0] for i in aux.SA_RANGES]
permSci = pd.DataFrame({
    'names': iVars,
    'mean': perm_importance['importances_mean'], 
    'std': perm_importance['importances_std']
})
shapImp = pd.DataFrame({
    'names': iVars,
    'mean': shapVals
})
permRF = impPM.reset_index()
permSci.to_csv(path.join(PT_OUT, fNameOut[:-4]+'_PMI-SCI.csv'), index=False)
permRF.to_csv(path.join(PT_OUT, fNameOut[:-4]+'_PMI-RFI.csv'), index=False)
shapImp.to_csv(path.join(PT_OUT, fNameOut[:-4]+'_SHP-SHP.csv'), index=False)
