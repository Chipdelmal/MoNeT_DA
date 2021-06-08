

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

if monet.isNotebook():
    (USR, LND, AOI, QNT, MTR) = ('dsk', 'PAN', 'HLT', '50', 'POE')
    JOB = aux.JOB_DSK
else:
    (USR, LND, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
    JOB = aux.JOB_SRV
EXPS = aux.getExps(LND)
MDLS = ('CPT', 'WOP', 'TTI', 'TTO', 'POE')
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
# Read ML
###############################################################################
fName = 'CLS_{}_{}Q_{}T_{}_RF.joblib'
fNameModel = [fName.format(AOI, QNT, int(float(aux.THS)*100), i) for i in MDLS]
mdls = [load(path.join(PT_OUT, i)) for i in fNameModel]
###############################################################################
# Evaluate ML
#   'i_sxm', 'i_sxg', 'i_sxn', 
#   'i_ren', 'i_res', 
#   'i_rsg', 'i_gsv', 'i_fcf', 
#   'i_mfm', 'i_mft', 'i_hrm', 'i_hrt', 
#   'i_grp', 'i_mig'
###############################################################################
sex = dbg.releasedSex(1)
(ren, res) = (2, .2)
(rsg, gsv) = (1e-5, 1e-8)
(hrm, hrt) = (0.786, 0.965)
fcf = 1
# Evaluate models at probe point ----------------------------------------------
vct = [[*sex, ren, res, rsg, gsv, fcf, 0.73, 0.93, hrm, hrt, 0, 0]]
{ix: i.predict(vct)[0] for (ix, i) in zip(MDLS, mdls)}
