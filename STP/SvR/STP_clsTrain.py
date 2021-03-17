
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


if monet.isNotebook():
    (MTR, THS, VT_SPLIT, KFOLD, QNT) = ('CPT', '0.5', '0.5', '50', '50')
else:
    (MTR, THS, VT_SPLIT, KFOLD, QNT) = (
        sys.argv[1], sys.argv[2], float(sys.argv[3]), 
        int(sys.argv[4]), sys.argv[5]
    )
QNTS = [QNT]
if (MTR == 'CPT') or (MTR == 'POE'):
    OUT_THS = [MTR]
else:
    OUT_THS = ['0.05', '0.1', '0.25', '0.5']
for label in OUT_THS:
    ###############################################################################
    # Setup constants (user input)
    ###############################################################################
    JOBS = 8
    (FEATS, LABLS) = (
        [
            'i_smx', 'i_sgv', 'i_sgn',
            'i_rsg', 'i_rer', 'i_ren', 'i_qnt', 'i_gsv', 'i_fic'
        ],
        [label]
    )
    # (VT_SPLIT, KFOLD) = (.5, 20)
    (TREES, DEPTH) = (30, 15)
    ###############################################################################
    # Create directories structure
    ###############################################################################
    PT_ROT = '/home/chipdelmal/Documents/WorkSims/STP/PAN/'
    (PT_IMG, PT_MOD, PT_OUT) = (
        PT_ROT+'img/', PT_ROT+'MODELS/', PT_ROT+'SUMMARY/'
    )
    ID_MTR = ['CLN_HLT_{}_{}_qnt.csv'.format(MTR, i) for i in QNTS]
    ###############################################################################
    # Load and inspect dataset
    ###############################################################################
    DTA_RAW = pd.concat([pd.read_csv(path.join(PT_OUT, i)) for i in ID_MTR])
    tS = datetime.now()
    monet.printExperimentHead(PT_OUT, PT_MOD, tS, 'UCIMI ML-Class Train '+MTR)
    if (MTR == 'CPT') or (MTR == 'POE'):
        DTA_TYPES = {
            'i_smx': np.bool_, 'i_sgv': np.bool_, 'i_sgn': np.bool_,
            'i_rsg': 'float64', 'i_rer': 'float64',
            'i_qnt': 'int8',
            'i_gsv': 'float64', 'i_fic': 'float64',
            'i_ren': 'int8',
            MTR: 'int8'
        }
    else:
        DTA_TYPES = {
            'i_smx': np.bool_, 'i_sgv': np.bool_, 'i_sgn': np.bool_,
            'i_rsg': 'float64', 'i_rer': 'float64',
            'i_qnt': 'int8',
            'i_gsv': 'float64', 'i_fic': 'float64',
            'i_ren': 'int8', '0.95': 'int8', '0.9':  'int8', '0.75': 'int8',
            '0.5':  'int8', '0.25': 'int8', '0.1':  'int8', '0.05': 'int8',
        }
    DTA_CLN = DTA_RAW.astype(DTA_TYPES)
    DTA_LEN = DTA_CLN.shape[0]
    correlation = DTA_CLN.corr(method='spearman')[LABLS][:len(FEATS)]
    ###############################################################################
    # Split dataset
    ###############################################################################
    (inputs, outputs) = (DTA_CLN[FEATS], DTA_CLN[LABLS])
    (TRN_X, VAL_X, TRN_Y, VAL_Y) = train_test_split(
        inputs, outputs, 
        test_size=float(VT_SPLIT), stratify=outputs
    )
    (TRN_L, VAL_L) = [i.shape[0] for i in (TRN_X, VAL_X)]
    ###############################################################################
    # Training Model
    ###############################################################################
    rf = RandomForestClassifier(
        n_estimators=TREES, max_depth=DEPTH, criterion='entropy',
        min_samples_split=5, min_samples_leaf=50,
        max_features=None, max_leaf_nodes=None,
        n_jobs=JOBS
    )
    # K-fold training -------------------------------------------------------------
    kScores = cross_val_score(
        rf, TRN_X, TRN_Y.values.ravel(), cv=int(KFOLD), 
        scoring=metrics.make_scorer(metrics.f1_score, average='weighted')
    )
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
        display_labels=list(range(len(set(TRN_Y[MTR])))),
        cmap=cm.Blues, normalize=None
    )
    featImportance = list(rf.feature_importances_)
    ###############################################################################
    # Statistics & Model Export
    ###############################################################################
    if (MTR == 'CPT') or (MTR == 'POE'):
        strMod = PT_MOD+ID_MTR[0][4:-8]
    else:
        strMod = PT_MOD+ID_MTR[0][4:-10]+str(int(float(LABLS[0])*100)).zfill(2)
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


###############################################################################
# PCA Tests
###############################################################################
# pca = PCA(n_components = 2)
# X2D = pca.fit_transform(TRN_X)
# X2DT = X2D.T
# plt.scatter(x=X2DT[0], y=X2DT[1])

