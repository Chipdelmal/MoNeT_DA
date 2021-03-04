
import sys
import numpy as np
import pandas as pd
from os import path
from datetime import datetime
from joblib import dump, load
import MoNeT_MGDrivE as monet
from treeinterpreter import treeinterpreter as ti
import PYF_aux as aux


if monet.isNotebook():
    (USR, LND, MTR, QNT, AOI) = ('dsk', 'PAN', 'WOP', '90', 'HLT')
else:
    (USR, LND, MTR, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

(FEATS, LABLS) = (['i_pop', 'i_ren', 'i_res', 'i_mad', 'i_mat'], ['0.1'])
###############################################################################
# Setting up paths
###############################################################################
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR, PT_MOD) = aux.selectPath(
    USR, LND
)
PT_IMG = PT_IMG + 'pstModel/'
monet.makeFolder(PT_IMG)
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
PTH_MOD = path.join(PT_MOD, ID_MTR[0:-8]+'_RF.joblib')
###############################################################################
# Load Model/Dataset
###############################################################################
rf = load(PTH_MOD)
df = pd.read_csv(path.join(PT_MTR, 'CLN_'+ID_MTR))
# Get variables ranges (entries) ----------------------------------------------
indepRanges = [sorted(list(df[j].unique())) for j in FEATS]
varRanges = {k: ran for (k, ran) in zip(FEATS, indepRanges)}
###############################################################################
# Probes
#   ['i_pop', 'i_ren', 'i_res', 'i_mad', 'i_mat']
###############################################################################
inProbe = [[16, 10, 2, 0, 0]]
# Classify and get probs ------------------------------------------------------
i=0
className = rf.predict(inProbe)
pred = rf.predict_log_proba(inProbe)
# Interpretations -------------------------------------------------------------
(prediction, biases, contributions) = ti.predict(rf, np.asarray(inProbe))
print("* Instance: {}".format(inProbe[i]))
predLog = ['{:.3f}'.format(100*j) for j in pred[i]]
predProb = ['{:.3f}'.format(j) for j in prediction[i]]
print('* Class: {} {}'.format(className[i], predProb))
for (c, feature) in zip(contributions[0], FEATS):
    ptest = '{:.4f}'.format(c[className[i]]).zfill(3)
    print('\t{}: {}'.format(feature, ptest))
###############################################################################
# Prediction SA
###############################################################################
(SMP, DSC) = (10, 2)
rankCenter = [abs(j[className[i]]) for j in contributions[0]]
rankHIx = rankCenter.index(max(rankCenter))
rankFeat = FEATS[rankHIx]
(ctrVal, deviation) = (inProbe[i][rankHIx], np.std(np.asarray(df[rankFeat])))
#sdP = sorted(list(np.random.normal(inProbe[i][rankHIx], deviation/10, size=SMP)))
(lo, hi) = (ctrVal-deviation/DSC, ctrVal+deviation/DSC)
sdP = np.arange(lo, hi, (hi-lo)/SMP)
# Perturb variable ------------------------------------------------------------
inCpy = []
for r in range(SMP):
    inCpy.append(inProbe[i][:])
for (r, row) in enumerate(inCpy):
    row[rankHIx] = sdP[r]
className = rf.predict(np.asarray(inCpy))
(prediction, biases, contributions) = ti.predict(rf, np.asarray(inCpy))
preds = list(zip(
    sdP,
    list(className), 
    [max(j) for j in prediction]
))
# Print summary ---------------------------------------------------------------
print('* SA [{}: {}]'.format(rankFeat, ctrVal))
for j in preds:
    print('\t{:.3f} - Class: {} - Prob: {:.3f}'.format(j[0], j[1], j[2]))