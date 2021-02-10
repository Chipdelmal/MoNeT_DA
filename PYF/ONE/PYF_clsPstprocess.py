
import sys
from os import path
from datetime import datetime
from joblib import dump, load
import MoNeT_MGDrivE as monet
import numpy as np
import PYF_aux as aux


if monet.isNotebook():
    (USR, LND, MTR, QNT, AOI) = ('dsk', 'PAN', 'WOP', '90', 'HLT')
else:
    (USR, LND, MTR, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

(FEATS, LABLS) = (
    ['i_pop', 'i_ren', 'i_res', 'i_mad', 'i_mat'],
    ['0.1']
)
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
monet.printExperimentHead(PT_DTA, PT_IMG, tS, 'PYF ClsPreprocess ')

ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
PTH_MOD = path.join(
    PT_MOD, ID_MTR[0:-8]+'_RF.joblib'
)
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