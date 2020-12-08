from joblib import dump, load
import MoNeT_MGDrivE as monet
import numpy as np


(MTR, QNT, JOBS) = ('WOP', '50', 4)
(FEATS, LABLS) = (
    [
        'i_smx', 'i_sgv', 'i_sgn',
        'i_rsg', 'i_rer', 'i_ren', 'i_gsv', 'i_fic'
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
PTH_MOD = PT_MOD+ID_MTR[4:-7]+str(int(float(LABLS[0])*100))+'_RF.joblib'
###############################################################################
# Load Model
###############################################################################
rf = load(PTH_MOD)
###############################################################################
# Probes
#   ['i_rer', 'i_ren', 'i_rsg', 'i_fic', 'i_gsv']
###############################################################################
print('* Testing...')
inProbe = [[True, False, False, .1, 1, 1e-2, 1, 1e-3]]
className = rf.predict(inProbe)
pred = rf.predict_log_proba(inProbe)
print('\t* Class [{}]'.format(className))
print('\t* Log-probs {}'.format(pred))

