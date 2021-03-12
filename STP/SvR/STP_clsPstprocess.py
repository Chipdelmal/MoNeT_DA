from joblib import dump, load
import MoNeT_MGDrivE as monet
import numpy as np
from treeinterpreter import treeinterpreter as ti


(MTR, QNT, JOBS) = ('WOP', '90', 4)
(FEATS, LABLS) = (
    [
        'i_smx', 'i_sgv', 'i_sgn',
        'i_rsg', 'i_rer', 'i_ren', 'i_qnt', 'i_gsv', 'i_fic'
    ],
    ['0.1']
)
###############################################################################
# Create directories structure
###############################################################################
ID_MTR = 'CLN_HLT_{}_{}_qnt.csv'.format(MTR, QNT)
PT_ROT = '/home/chipdelmal/Documents/WorkSims/STP/PAN/'
(PT_IMG, PT_MOD, PT_OUT) = (
    PT_ROT+'img/', PT_ROT+'MODELS/', PT_ROT+'SUMMARY/'
)
ID_MTR = 'CLN_HLT_{}_{}_qnt.csv'.format(MTR, QNT)
PTH_MOD = PT_MOD+ID_MTR[4:-10]+str(int(float(LABLS[0])*100))+'_RF.joblib'
###############################################################################
# Load Model
###############################################################################
rf = load(PTH_MOD)
###############################################################################
# Probes
#   ['i_rsg', 'i_rer', 'i_ren', 'i_qnt', 'i_gsv', 'i_fic']
###############################################################################
inProbe = [[True, False, False, .1, 1, 5, .5, 1e-3, .001]]
# Classify and get probs ------------------------------------------------------
i=0
className = rf.predict(inProbe)
pred = rf.predict_log_proba(inProbe)
print("* Instance: {}".format(inProbe[i]))
predStr = ['{:.3f}'.format(100*j) for j in pred[i]]
print('* Class: {} {}'.format(className[i], predStr))
# Interpretations -------------------------------------------------------------
(prediction, biases, contributions) = ti.predict(rf, np.asarray(inProbe))
print("* Bias (trainset mean): {}".format(biases[i]))
for c, feature in zip(contributions[0], FEATS):
    ptest = '{:.4f}'.format(c[className[i]]).zfill(3)
    print('\t{}: {}'.format(feature, ptest))
