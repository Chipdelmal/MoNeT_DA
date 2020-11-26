

from os import path
import numpy as np
import pandas as pd
from joblib import dump
from matplotlib.pyplot import cm
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier


###############################################################################
# Setup constants (user input)
###############################################################################
(MTR, QNT) = ('WOP', '50')
(FEATS, LABLS) = (
    [
        'i_smx', 'i_sgv', 'i_sgn',
        'i_rsg', 'i_rer', 'i_ren', 'i_gsv', 'i_fic'
    ],
    ['0.1']
)
(VT_SPLIT, KFOLD) = (.5, 20)
(TREES, DEPTH) = (8, 8)
###############################################################################
# Create directories structure
###############################################################################
ID_MTR = 'CLN_HLT_{}_{}_qnt.csv'.format(MTR, QNT)
PT_ROT = '/home/chipdelmal/Documents/WorkSims/STP/PAN/'
(PT_IMG, PT_MOD, PT_OUT) = (
    PT_ROT+'img/', PT_ROT+'MODELS/', PT_ROT+'SUMMARY/'
)
ID_MTR = 'CLN_HLT_{}_{}_qnt.csv'.format(MTR, QNT)
###############################################################################
# Load and inspect dataset
###############################################################################
DTA_RAW = pd.read_csv(path.join(PT_OUT, ID_MTR))
DTA_TYPES = {
    'i_smx': np.bool_, 'i_sgv': np.bool_, 'i_sgn': np.bool_,
    'i_rsg': 'float64', 'i_rer': 'float64',
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
    inputs, outputs, test_size=VT_SPLIT
)
(TRN_L, VAL_L) = [i.shape[0] for i in (TRN_X, VAL_X)]
###############################################################################
# Training Model
###############################################################################
rf = RandomForestClassifier(n_estimators=TREES, max_depth=DEPTH)
# K-fold training -------------------------------------------------------------
kScores = cross_val_score(rf, TRN_X, TRN_Y, cv=KFOLD)
# Final training --------------------------------------------------------------
rf.fit(TRN_X, TRN_Y)
PRD_Y = rf.predict(VAL_X)
accuracy = metrics.accuracy_score(VAL_Y, PRD_Y)
confusionMat = metrics.plot_confusion_matrix(
    rf, VAL_X, VAL_Y, 
    display_labels=['None', 'Low', 'Mid', 'Full'],
    cmap=cm.Blues, normalize='pred'
)
featImportance = list(rf.feature_importances_)
###############################################################################
# Statistics
###############################################################################
print('* Train/Validate entries: {}/{} ({})'.format(TRN_L, VAL_L, TRN_L+VAL_L))
print('* Cross-validation: %0.2f (+/-%0.2f)'%(kScores.mean(), kScores.std()*2))
print('* Validation Accuracy: {:.2f}'.format(accuracy))
print('* Features importance & correlation')
for i in zip(FEATS, featImportance, correlation[LABLS[0]]):
    print('\t* {}: {:.3f}, {:.3f}'.format(*i))
###############################################################################
# Export
###############################################################################
strMod = PT_MOD+ID_MTR[4:-7]+'RF.joblib'
dump(rf, strMod)
