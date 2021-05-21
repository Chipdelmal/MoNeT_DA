

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
from contextlib import redirect_stdout
from pdpbox import pdp, get_dataset, info_plots
from sklearn.inspection import partial_dependence, plot_partial_dependence
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd


if monet.isNotebook():
    (USR, LND, AOI, QNT, MTR) = ('dsk', 'PAN', 'HLT', '50', 'POE')
    VT_SPLIT = aux.VT_TRAIN
else:
    (USR, LND, AOI, QNT, MTR) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
    VT_SPLIT = aux.VT_TRAIN
EXPS = aux.getExps(LND)
(TREES, DEPTH, KFOLD) = (aux.TREES, aux.DEPTH, aux.KFOLD)
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
###############################################################################
# Paths
###############################################################################
(drive, land) = (
    drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND)
)
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
# Time and head --------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_OUT, tS, 
    '{} ClsTrain [{}:{}:{}:{}]'.format(aux.XP_ID, aux.DRV, QNT, AOI, MTR)
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
(f, ax) = plt.subplots(figsize=(10, 8))
sns.heatmap(
    correlation, mask=np.zeros_like(correlation, dtype=np.bool), 
    cmap=sns.diverging_palette(220, 10, as_cmap=True),
    square=True, ax=ax
)
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
confusionMat = metrics.plot_confusion_matrix(
    rf, VAL_X, VAL_Y, 
    # display_labels=list(range(len(set(outputs[outputs.columns[0]])))),
    cmap=cm.Blues, normalize=None
)
plt.savefig(modelPath+'_RF.jpg', dpi=300)
# Features importance ---------------------------------------------------------
featImportance = list(rf.feature_importances_)
impDC = rfp.oob_dropcol_importances(rf, TRN_X, TRN_Y.values.ravel())
impDCD = impDC.to_dict()['Importance']
impPM = rfp.importances(rf, TRN_X, TRN_Y)
impPMD = impPM.to_dict()['Importance']
viz = rfp.plot_corr_heatmap(DATA, figsize=(7,5))
###############################################################################
# Interpretability Plots
###############################################################################
# feat = FEATS[3]
# for feat in FEATS:
#     isolate = pdp.pdp_isolate(
#         model=rf, dataset=TRN_X, model_features=FEATS, feature=feat
#     )
#     fracPlot = 2500
#     (fig, axes) = pdp.pdp_plot(
#         pdp_isolate_out=isolate, feature_name=feat,
#         center=False, x_quantile=True, plot_pts_dist=False,
#         ncols=len(list(rf.classes_)), plot_lines=True, frac_to_plot=fracPlot,
#         plot_params = {
#             'line_cmap': 'Blues',
#             'subtitle_fontsize': 1, 'xticks_rotation': 0,
#             'pdp_linewidth': .5, 'zero_linewidth': 0.1,
#             'pdp_color': '#ff006e', 'pdp_hl_color': '#ff006e',
#             'fill_color': '#ff006e', 'zero_color': '#ff006e',
#             'fill_alpha': 0.25, 'markersize': 0.05,
#         }
#     )
#     axes['title_ax'].set_visible(False)
#     for ax in axes['pdp_ax']:
#         ax.tick_params(axis='both', which='major', labelsize=3)
#         ax.set_xlabel('')
#         ax.set_ylim(-0, 1.1)
#         xDiff = (ax.get_xlim()[1]-ax.get_xlim()[0])
#         yDiff = (ax.get_ylim()[1]-ax.get_ylim()[0])
#         for (i, trc) in enumerate(ax.get_lines()):
#             if (i<fracPlot):
#                 trc.set_color('#a2d2ff')
#                 trc.set_linewidth(.1)
#                 trc.set_alpha(.2)
#     fig.subplots_adjust(hspace=2)
#     fig.tight_layout()
#     fig.savefig(
#         modelPath+'_ICE'+'_'+feat.split('_')[-1]+'.jpg', 
#         dpi=1000, bbox_inches='tight', pad_inches=0.1
#     )
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

