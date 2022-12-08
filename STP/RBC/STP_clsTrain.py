

import sys
from glob import glob
from datetime import datetime
from os import path
from re import match
import numpy as np
import pandas as pd
import rfpimp as rfp
import seaborn as sns
from joblib import dump
from sklearn import metrics
import compress_pickle as pkl
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from math import radians
from contextlib import redirect_stdout
# from pdpbox import pdp, get_dataset, info_plots
from sklearn.inspection import partial_dependence, plot_partial_dependence
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd


if monet.isNotebook():
    (USR, LND, AOI, DRV, QNT, MTR) = ('srv', 'PAN', 'HLT', 'LDR', '50', 'WOP')
    VT_SPLIT = aux.VT_TRAIN
else:
    (USR, LND, AOI, DRV, QNT, MTR) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
    )
    VT_SPLIT = aux.VT_TRAIN
EXPS = aux.getExps(LND)
(TREES, DEPTH, KFOLD) = (aux.TREES, aux.DEPTH, aux.KFOLD)
TICKS_HIDE = True
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
###############################################################################
# Paths
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND)
)
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND, DRV)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
(scalers, HD_DEP, _, cmap) = aux.selectDepVars(MTR, AOI)
# Time and head --------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_OUT, tS, 
    '{} ClsTrain [{}:{}:{}:{}]'.format(aux.XP_ID, DRV, QNT, AOI, MTR)
)
###############################################################################
# Read CSV
###############################################################################
(fName_I, fName_R, fName_C) = (
    'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, int(float(aux.THS)*100)),
    'REG_{}_{}Q_{}T.csv'.format(AOI, QNT, int(float(aux.THS)*100)),
    'CLS_{}_{}Q_{}T.csv'.format(AOI, QNT, int(float(aux.THS)*100)),
)
DATA = pd.read_csv(path.join(PT_OUT, fName_C))
modelPath = path.join(PT_OUT, fName_C.split('.')[0]+'_'+MTR)
modelImg = path.join(PT_OUT, 'img', fName_C.split('.')[0]+'_'+MTR)
# Features and labels ---------------------------------------------------------
COLS = list(DATA.columns)
(FEATS, LABLS) = (
    [i for i in COLS if i[0]=='i'],
    [i for i in COLS if i[0]!='i']
)
###############################################################################
# Pre-Analysis
###############################################################################
correlation = DATA.corr(method='spearman')
# (f, ax) = plt.subplots(figsize=(10, 8))
# sns.heatmap(
#     correlation, mask=np.zeros_like(correlation, dtype=np.bool), 
#     cmap=sns.diverging_palette(220, 10, as_cmap=True),
#     square=True, ax=ax
# )
# f.show()
###############################################################################
# Split Train/Test
###############################################################################
(inputs, outputs) = (DATA[FEATS], DATA[MTR])
(TRN_X, VAL_X, TRN_Y, VAL_Y) = train_test_split(
    inputs, outputs, 
    test_size=float(VT_SPLIT),
    stratify=outputs
)
(TRN_L, VAL_L) = [i.shape[0] for i in (TRN_X, VAL_X)]
###############################################################################
# Training Model
###############################################################################
rf = RandomForestClassifier(
    n_estimators=TREES, max_depth=DEPTH, criterion='entropy',
    min_samples_split=5, min_samples_leaf=50,
    max_features=None, max_leaf_nodes=None,
    n_jobs=JOB
)
# K-fold training -------------------------------------------------------------
kScores = cross_val_score(
    rf, TRN_X, TRN_Y.values.ravel(), 
    cv=int(KFOLD), 
    scoring=metrics.make_scorer(metrics.f1_score, average='weighted')
)
outLabels = set(list(TRN_Y.values.ravel()))
# Final training --------------------------------------------------------------
rf.fit(TRN_X, TRN_Y.values.ravel())
PRD_Y = rf.predict(VAL_X)
(accuracy, f1, precision, recall, jaccard) = (
    metrics.accuracy_score(VAL_Y, PRD_Y),
    metrics.f1_score(VAL_Y, PRD_Y, average='weighted'),
    metrics.precision_score(VAL_Y, PRD_Y, average='weighted'),
    metrics.recall_score(VAL_Y, PRD_Y, average='weighted'),
    metrics.jaccard_score(VAL_Y, PRD_Y, average='weighted')
)
report = metrics.classification_report(VAL_Y, PRD_Y)
plt.rcParams.update({'font.size': 7})
confusionMat = metrics.plot_confusion_matrix(
    rf, VAL_X, VAL_Y, 
    # display_labels=list(range(len(set(outputs[outputs.columns[0]])))),
    cmap=cmap, normalize=None
)
plt.savefig(modelPath+'_RF.png', dpi=750, bbox_inches='tight', pad_inches=0.2)
# Features importance ---------------------------------------------------------
featImportance = list(rf.feature_importances_)
impDC = rfp.oob_dropcol_importances(rf, TRN_X, TRN_Y.values.ravel())
impDCD = impDC.to_dict()['Importance']
impPM = rfp.importances(rf, TRN_X, TRN_Y)
impPMD = impPM.to_dict()['Importance']
# viz = rfp.plot_corr_heatmap(DATA, figsize=(7,5))
###############################################################################
# Statistics & Model Export
###############################################################################
# plt.savefig(modelPath+'_RF.jpg', dpi=300)
dump(rf, modelPath+'_RF.joblib')
with open(modelPath+'_RF.txt', 'w') as f:
    with redirect_stdout(f):
        print('* Feats Order: {}'.format(FEATS))
        print('* Train/Validate entries: {}/{} ({})'.format(TRN_L, VAL_L, TRN_L+VAL_L))
        print('* Cross-validation F1: %0.2f (+/-%0.2f)'%(kScores.mean(), kScores.std()*2))
        print('* Validation Accuracy: {:.2f}'.format(accuracy))
        print('* Validation F1: {:.2f} ({:.2f}/{:.2f})'.format(f1, precision, recall))
        print('* Jaccard: {:.2f}'.format(jaccard))
        print('* Features Importance & Correlation')
        for i in zip(FEATS, featImportance, correlation[LABLS[0]]):
            print('\t* {}: {:.3f}, {:.3f}'.format(*i))
        print('* Drop-Cols & Permutation Features Importance')
        for i in FEATS:
            print('\t* {}: {:.3f}, {:.3f}'.format(i, impDCD[i], impPMD[i]))
        print('* Class report: ')
        print(report)
with open(modelPath+'_RFI.csv', 'w') as f:
    for i in FEATS:
        print('{}, {:.3f}, {:.3f}'.format(i, impDCD[i], impPMD[i]))
###############################################################################
# Statistics & Model Export
###############################################################################
plotSort = [
    'i_fch', 'i_fcb', 'i_fcr', 'i_hrm', 'i_hrf', 'i_rsg',
    'i_gsv',
    'i_ren', 'i_res',
    'i_sxm', 'i_sxg', 'i_sxn'
]
plotSort.reverse()
COLS = list(DATA.columns)
(FEATS, LABLS) = (
    [i for i in COLS if i[0]=='i'],
    [i for i in COLS if i[0]!='i']
)
FEATS.remove('i_mig')
FEATS.remove('i_grp')
col = [i[2] for i in aux.DICE_PARS if i[0]==MTR][0]
(fig, ax) = plt.subplots(figsize=(3, 10), ncols=1, sharey=True)
ax.barh(
    plotSort, 
    [impDCD[i] for i in plotSort], #sorted(FEATS, reverse=True)], 
    align='center', zorder=10, 
    color=col[:-2]+'AA',
    height=0.9
)
ax.grid(1)
ax.set_xlim(0, .5)
ax.xaxis.set_ticks(np.arange(0, .5, .125))
# ax.yaxis.set_ticks(np.arange(0, len(FEATS), 1))
if TICKS_HIDE:
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    # ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    # ax.xaxis.set_tick_params(width=0)
    # ax.yaxis.set_tick_params(width=0)
    ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    ax.set_axis_off()
fig.tight_layout()
fig.savefig(
    path.join(PT_IMG, 'FIMP_{}.png'.format(MTR)), 
    dpi=750, bbox_inches='tight', pad_inches=0, transparent=True
)



# (cat, val) = (list(impDC['Importance'].index), list(impDC['Importance'].values))
# polarBarChart(
#     cat, val, 
#     ticksStep=5,
#     colors=['#000000']*len(cat),
#     rRange=(0, 180)
# )
# def polarBarChart(
#         xVals, yVals,
#         figAx=None,
#         logScale=False, ticksStep=10,
#         rRange=(0, 270), yRange=None,
#         colors=['#000000'],
#         labels=True, labelQty=False,
#         origin='N', direction=1,
#         ticksFmt={
#             'lw': 1, 'range': (-0.5, -0.25), 
#             'color': '#000000DD', 'fontsize': 8, 'fmt': '{:.1f}'
#         },
#         labelFmt={
#             'color': '#000000EE', 'fontsize': 10, 
#             'ha': 'left', 'fmt': '{:.1f}'
#         }
#     ):
#     # Generate (fig, ax) if needed --------------------------------------------
#     if figAx is None:
#         (fig, ax) = plt.subplots(
#             figsize=(8, 8), subplot_kw={"projection": "polar"}
#         )
#     else:
#         (fig, ax) = figAx
#     # Get value ranges --------------------------------------------------------
#     (minValY, maxValY) = [
#         0 if not yRange else yRange[0],
#         max(yVals) if not yRange else yRange[1]
#     ]
#     if not yRange:
#         yRange = (minValY, maxValY)
#     # Define grid -------------------------------------------------------------
#     stepSizeY = maxValY/ticksStep
#     gridY = np.arange(minValY, maxValY+maxValY/stepSizeY, stepSizeY)
#     # Log-scale if needed -----------------------------------------------------
#     if logScale:
#         (gridYSca, yValsSca, yRangeSca) =  [
#             [log10(i+1) for i in j] for j in (gridY, yVals, yRange)
#         ]
#     else:
#         (gridYSca, yValsSca, yRangeSca) =  (gridY, yVals, yRange)
#     # Convert heights into radii ----------------------------------------------
#     (angleHeights, grids) = [
#         [np.interp(i, yRangeSca, rRange) for i in j] 
#         for j in (yValsSca, gridYSca)
#     ]
#     # Generate Plot -----------------------------------------------------------
#     for (i, ang) in enumerate(angleHeights):
#         ax.barh(i, radians(ang), color=colors[i])
#     # Gridlines and axes ------------------------------------------------------
#     ax.vlines(
#         [radians(i) for i in grids[:ticksStep+1]], 
#         len(xVals)+ticksFmt['range'][0], len(xVals)+ticksFmt['range'][1],
#         colors=ticksFmt['color']
#     )
#     ax.xaxis.grid(False)
#     ax.yaxis.grid(False)
#     ax.set_ylim(-.5, len(yVals)-0.1)
#     ax.spines['polar'].set_visible(False)
#     ax.set_theta_zero_location(origin)
#     ax.set_theta_direction(direction)
#     ax.set_rlabel_position(0)
#     # Labels ------------------------------------------------------------------
#     labelsText = [ticksFmt['fmt'].format(i) for i in gridY] if labels else []
#     ax.set_thetagrids(
#         grids[:ticksStep+1], labelsText[:ticksStep+1], 
#         color=ticksFmt['color']
#     )
#     # Categories Markers ------------------------------------------------------
#     if labelQty:
#         labelText = [
#             f' {w} ('+labelFmt['fmt'].format(v)+')' for (w, v) in zip(xVals, yVals)
#         ]
#     else:
#         labelText = [f' {i}' for i in xVals]
#     ax.set_rgrids(
#         [i for i in range(len(xVals))], 
#         labels=labelText,
#         va='center', **labelFmt
#     )
#     # Return results ----------------------------------------------------------
#     return (fig, ax)