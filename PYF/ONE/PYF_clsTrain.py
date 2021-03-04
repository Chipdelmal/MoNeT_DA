
import sys
from os import path
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import dump
from matplotlib.pyplot import cm
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.decomposition import PCA
import MoNeT_MGDrivE as monet
from contextlib import redirect_stdout
import PYF_aux as aux



if monet.isNotebook():
    (USR, LND, MTR, QNT, VT_SPLIT, KFOLD) = (
        'dsk', 'PAN', 'WOP', '90', .25, 10
    )
    JOBS = 4
else:
    (USR, LND, MTR, QNT, VT_SPLIT, KFOLD) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], 
        float(sys.argv[5]), int(sys.argv[6])
    )
    JOBS = 20
QNTS = [QNT, ]
OUT_THS = ['0.95', '0.9', '0.75', '0.5', '0.25', '0.1', '0.05']
###############################################################################
# Setting up paths
###############################################################################
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR, PT_MOD) = aux.selectPath(
    USR, LND
)
PT_IMG = PT_IMG + 'pstModel/'
monet.makeFolder(PT_IMG)
tS = datetime.now()
monet.printExperimentHead(PT_DTA, PT_IMG, tS, 'PYF ClsTrain ')

for label in OUT_THS:
    ###########################################################################
    # Setup constants (user input)
    ###########################################################################
    JOBS = 8
    (FEATS, LABLS) = (
        ['i_pop', 'i_ren', 'i_res', 'i_mad', 'i_mat'],
        [label]
    )
    (TREES, DEPTH) = (30, 6)
    ID_MTR = ['CLN_HLT_{}_{}_qnt.csv'.format(MTR, i) for i in QNTS]
    ###########################################################################
    # Load and inspect dataset
    ###########################################################################
    DTA_RAW = pd.concat([pd.read_csv(path.join(PT_MTR, i)) for i in ID_MTR])
    tS = datetime.now()
    monet.printExperimentHead(PT_MTR, PT_MOD, tS, 'PYF ML ClsTrain '+MTR)
    DTA_TYPES = {
        'i_pop': 'int8', 'i_ren': 'int8', 
        'i_res': 'float64', 'i_mad': 'float64', 'i_mat': 'float64'
    }
    DTA_CLN = DTA_RAW.astype(DTA_TYPES)
    DTA_LEN = DTA_CLN.shape[0]
    correlation = DTA_CLN.corr(method='spearman')[LABLS][:len(FEATS)]
    ###########################################################################
    # Split dataset
    ###########################################################################
    (inputs, outputs) = (DTA_CLN[FEATS], DTA_CLN[LABLS])
    (TRN_X, VAL_X, TRN_Y, VAL_Y) = train_test_split(
        inputs, outputs, 
        test_size=VT_SPLIT, stratify=outputs
    )
    (TRN_L, VAL_L) = [i.shape[0] for i in (TRN_X, VAL_X)]
    ###########################################################################
    # Training Model
    ###########################################################################
    rf = RandomForestClassifier(
        n_estimators=TREES, max_depth=DEPTH, criterion='entropy',
        min_samples_split=5, min_samples_leaf=50,
        max_features=None, max_leaf_nodes=None,
        n_jobs=JOBS
    )
    # K-fold training ---------------------------------------------------------
    kScores = cross_val_score(
        rf, TRN_X, TRN_Y.values.ravel(), 
        cv=KFOLD, scoring=metrics.make_scorer(metrics.f1_score, average='weighted')
    )
    # Final training ----------------------------------------------------------
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
        display_labels=['None', 'Transient', 'Permanent'],
        cmap=cm.Blues, normalize=None
    )
    featImportance = list(rf.feature_importances_)
    ###########################################################################
    # Statistics & Model Export
    ###########################################################################
    strMod = path.join(
        PT_MOD, ID_MTR[0][4:-10]+str(int(float(LABLS[0])*100)).zfill(2)
    )
    plt.savefig(strMod+'_RF.jpg', dpi=300)
    dump(rf, strMod+'_RF.joblib')
    with open(strMod+'_RF.txt', 'w') as f:
        with redirect_stdout(f):
            print('* Feats Order: {}'.format(list(DTA_CLN.columns)))
            print('* Train/Validate entries: {}/{} ({})'.format(TRN_L, VAL_L, TRN_L+VAL_L))
            print('* Cross-validation F1: %0.2f (+/-%0.2f)'%(kScores.mean(), kScores.std()*2))
            print('* Validation Accuracy: {:.2f}'.format(accuracy))
            print('* Validation F1: {:.2f} ({:.2f}/{:.2f})'.format(f1, precision, recall))
            print('* Jaccard: {:.2f}'.format(jaccard))
            print('* Features importance & correlation')
            for i in zip(FEATS, featImportance, correlation[LABLS[0]]):
                print('\t* {}: {:.3f}, {:.3f}'.format(*i))
            print('* Class report: ')
            print(report)