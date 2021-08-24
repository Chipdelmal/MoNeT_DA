

import sys
from os import path
from re import match
from glob import glob
from joblib import dump, load
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn import preprocessing
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
from treeinterpreter import treeinterpreter as ti

if monet.isNotebook():
    (USR, LND, AOI, QNT, DRV, MTR) = ('lab', 'PAN', 'HLT', '50', 'LDR', 'CPT')
    JOB = aux.JOB_DSK
else:
    (USR, LND, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], 
        sys.argv[4], sys.argv[5], sys.argv[6]
    )
    JOB = aux.JOB_SRV
EXPS = aux.getExps(LND)
MDLS = ('CPT', 'WOP', 'POE')
###############################################################################
# Paths
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND)
)
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND, DRV)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
###############################################################################
# Read ML
###############################################################################
fName = 'CLS_{}_{}Q_{}T_{}_RF.joblib'
fNameModel = [fName.format(AOI, QNT, int(float(aux.THS)*100), i) for i in MDLS]
mdls = [load(path.join(PT_OUT, i)) for i in fNameModel]
###############################################################################
# Evaluate ML
#   'i_sxm', 'i_sxg', 'i_sxn',
#   'i_fcb', 'i_fch', 'i_fcr',
#   'i_grp',
#   'i_gsv',
#   'i_hrf', 'i_hrm',
#   'i_mig',
#   'i_ren', 'i_res',
#   'i_rsg'
FEATS = [
    'i_sxm', 'i_sxg','i_sxn', 'i_fcb', 'i_fch', 'i_fcr',
    'i_grp', 'i_gsv', 'i_hrf', 'i_hrm', 'i_mig', 'i_ren',
    'i_res', 'i_rsg'
]
###############################################################################
sex = dbg.releasedSex(1)
(ren, res) = (5, .5)
(rsg, gsv) = (0, 1e-2)
(hrm, hrf) = (1, 0.956)
(fch, fcb, fcr) = (0.175, 0.117, 0)
# Evaluate models at probe point ----------------------------------------------
vct = [[*sex, fcb, fch, fcr, 0, gsv, hrf, hrm, 0, ren, res, rsg]]
{ix: i.predict(vct)[0] for (ix, i) in zip(MDLS, mdls)}
{ix: ti.predict(i, np.asarray(vct)) for (ix, i) in zip(MDLS, mdls)}
# -----------------------------------------------------------------------------
i=0
rf = mdls[1]
pred = rf.predict_log_proba(vct)
(prediction, biases, contributions) = ti.predict(rf, np.asarray(vct))
print("* Instance: {}".format(vct))
predLog = ['{:.3f}'.format(100*j) for j in pred[i]]
predProb = ['{:.3f}'.format(j) for j in prediction[i]]
print('* Class: {}'.format(predProb))
for (c, feature) in zip(contributions[0], FEATS):
    ptest = '{:.4f}'.format(c[i]).zfill(3)
    print('\t{}: {}'.format(feature, ptest))