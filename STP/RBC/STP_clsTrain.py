

import sys
from glob import glob
from datetime import datetime
from os import path
from re import match
import numpy as np
import pandas as pd
import rfpimp as rfp
import seaborn as sns
from sklearn import metrics
import compress_pickle as pkl
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd


if monet.isNotebook():
    (USR, LND, AOI, QNT, MTR) = ('dsk', 'PAN', 'HLT', '90', 'CPT')
    VT_SPLIT = 0.3
    JOB = aux.JOB_DSK
else:
    (USR, LND, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
    VT_SPLIT = sys.argv[6]
    JOB = aux.JOB_SRV
EXPS = aux.getExps(LND)
(TREES, DEPTH, KFOLD) = (aux.TREES, aux.DEPTH, aux.KFOLD)
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
###############################################################################
# Load DF
###############################################################################
fName_I = 'CLN_{}_{}_{}_qnt.csv'.format(AOI, MTR, QNT)
DATA = pd.read_csv(path.join(PT_OUT, fName_I))
COLS = list(DATA.columns)
(FEATS, LABLS) = (
    [i for i in COLS if i[0]=='i'],
    [i for i in COLS if i[0]!='i']
)
###############################################################################
# Pre-Analysis
###############################################################################
correlation = DATA.corr(method='spearman')
f, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    correlation, mask=np.zeros_like(correlation, dtype=np.bool), 
    cmap=sns.diverging_palette(220, 10, as_cmap=True),
    square=True, ax=ax
)
f.show()
###############################################################################
# Split Train/Test
###############################################################################
(inputs, outputs) = (DATA[FEATS], DATA[LABLS])
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
    display_labels=list(range(len(set(outputs[outputs.columns[0]])))),
    cmap=cm.Blues, normalize=None
)
# Features importance ---------------------------------------------------------
featImportance = list(rf.feature_importances_)
impDC = rfp.oob_dropcol_importances(rf, TRN_X, TRN_Y.values.ravel())
impDCD = impDC.to_dict()['Importance']
impPM = rfp.importances(rf, TRN_X, TRN_Y)
impPMD = impPM.to_dict()['Importance']
