
import os
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from os import path
import pandas as pd
from joblib import dump, load
import MoNeT_MGDrivE as monet
from sklearn import metrics
from sklearn.metrics import plot_confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import STP_dataAnalysis as da


###############################################################################
# Inputs breakdown: 
#   i_sex: Sex of the releases
#   i_rer: Release ratio (number of mosquitoes released as compared to total)
#   i_ren: Release number (number of weekly released)
#   i_rsg: Resistance generation (non-cleavable genotypes)
#   i_fic: Fitness cost (sterility)
#   i_gsv: Genetic standing vatiation (similar to resistance)
###############################################################################
(MTR, ERR, OVW, THS, QNT) = ('WOP', False, True, '0.1', '50')
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
FEATS = ['i_sex', 'i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv', 'i_grp']
(ESTRS, DPTH) = (10, 8)
# Classifier Variables --------------------------------------------------------
(OPRAN, TV_SPLT) = (((0, 1), (1, 2), (2, 3), (3, 5), (5, 10)), .25)
(modelFeats, classNames) = (
    ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv'],
    ['None', 'Low', 'Mid', 'High', 'Permanent']
)
###############################################################################
# Create directories structure
###############################################################################
PT_ROT = '/home/chipdelmal/Documents/WorkSims/STP/PAN/'
PT_OUT = PT_ROT + 'SUMMARY/'
PT_DTA = '{}{}_{}'.format(PT_OUT, 'Full', ID_MTR)
PT_IMG = PT_ROT + 'img/'
PT_MOD = PT_ROT + 'MODELS/'
[monet.makeFolder(i) for i in (PT_OUT, PT_MOD)]
###############################################################################
# Read and clean datasets
###############################################################################
print('* Reading datasets...')
dfRC = da.rescaleDataset(pd.read_csv(PT_DTA), 1)
data = dfRC.drop(dfRC.columns[0], axis=1)
HEADER = list(dfRC.columns)
LBLS = sorted(list(set(HEADER) - set(FEATS))),
FEATS_LVLS = {i: list(data[i].unique()) for i in FEATS}
###############################################################################
# Preprocess
###############################################################################
print('* Filtering datasets...')
# Select dataset and create filter rules --------------------------------------
filterRules = (
    data['i_grp'] == 0,
    # data['i_sex'] == 'gravidFemale'
)
# Filter with rules -----------------------------------------------------------
fltr = [all(i) for i in zip(*filterRules)]
dataFiltered = data[fltr]
corrScores = dataFiltered.corr(method='spearman')[THS][modelFeats]
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(np.array(dataFiltered['i_sex']))
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
inverted = label_encoder.inverse_transform([np.argmax(onehot_encoded[0, :])])
# Calculate Operational Ranges ------------------------------------------------
grpMtr = np.asarray(dataFiltered[THS])
groupBools = [[i[0]*365 <= feat < i[1]*365 for i in OPRAN] for feat in grpMtr]
set(tuple(i) for i in groupBools)
groupIx = [i.index(True) for i in groupBools]
# Features/Labels Separate ----------------------------------------------------
(features, labels) = (dataFiltered[modelFeats], groupIx)
###############################################################################
# Split and preprocess dataset
###############################################################################
print('* Splitting')
(xtrn, xval, ytrn, yval) = train_test_split(
    features, labels, test_size=TV_SPLT
)
(trnSize, valSize) = (len(xtrn), len(xval))
totalSize = valSize + trnSize
print('\t* Train entries: {} ({})'.format(trnSize, trnSize/totalSize))
print('\t* Validate entries: {} ({})'.format(valSize, valSize/totalSize))
print('\t* Total entries: {} '.format(totalSize))
sc = StandardScaler()
xtrn = sc.fit_transform(xtrn)
xval = sc.transform(xval)
###############################################################################
# Train
###############################################################################
strMod = PT_MOD + 'RandomForest.joblib'
if (not path.exists(strMod)) or (OVW):
    print('* Cross validating...')
    rf = RandomForestClassifier(n_estimators=ESTRS, max_depth=DPTH)
    # Cross-Validate ----------------------------------------------------------
    scores = cross_val_score(rf, xtrn, ytrn, cv=10)
    print('\t* Accuracy: %0.3f (+/- %0.2f)' % (scores.mean(), scores.std()*2))
    # Train -------------------------------------------------------------------
    print('* Training...')
    rf = RandomForestClassifier(n_estimators=ESTRS, max_depth=DPTH)
    rf.fit(xtrn, ytrn)
    dump(rf, strMod)
else:
    print('* Loading...')
    rf = load(strMod)
###############################################################################
# Metrics
###############################################################################
print('* Validating...')
ypred = rf.predict(xval)
print('\t* Accuracy: {:.3f}'.format(metrics.accuracy_score(yval, ypred)))
print('* Feature Correlations and Importances...')
for i in zip(modelFeats, corrScores, rf.feature_importances_):
    print('\t* {}: \t{:.3f} \t{:.3f}'.format(*i))
plot_confusion_matrix(
    rf, xval, yval,
    display_labels=classNames, cmap=plt.cm.Blues,
    normalize=None
)
print(classification_report(yval, ypred, target_names=classNames))
###############################################################################
# Probes
#   ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv']
###############################################################################
print('* Testing...')
FEATS_LVLS
inProbe = [.1, 1, 1e-2, 1, 1e-3]
inTransform = sc.transform([inProbe])
className = classNames[rf.predict(inTransform)[0]]
pred = rf.predict_log_proba(inTransform)
print('\t* Class [{}]'.format(className))
print('\t* Log-probs {}'.format(pred))

# scatter_matrix(dataFiltered[modelFeats], figsize=(12, 8))
