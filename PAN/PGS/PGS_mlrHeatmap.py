import sys
import numpy as np
from os import path
import pandas as pd
import compress_pickle as pkl
from datetime import datetime
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
import PGS_aux as aux
import PGS_gene as drv
import PGS_mlrMethods as mth

if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'PGS', '50', 'HLT', '0.1', 'WOP')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
iVars = ['i_fvb', 'i_mfr', 'i_ren']
# iVars = ['i_ren', 'i_res', 'i_fvb']
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
# Params Scaling --------------------------------------------------------------
(xSca, ySca) = ('linear', 'linear')
TICKS_HIDE = True
MAX_TIME = 365*2
CLABEL_FONTSIZE = 0
(HD_IND, kSweep) = ([iVars[0], iVars[1]], iVars[2]) 
###############################################################################
# Paths
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, fldr)
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_OUT, tS, 
    '{} mlrHeatmap [{}:{}:{}]'.format(DRV, AOI, THS, MOI)
)
###############################################################################
# Select Model and Scores
###############################################################################
(MOD_SEL, K_SPLITS, T_SIZE) = ('mlp', 10, .1)
###############################################################################
# Load Model
###############################################################################
fNameOut = '{}_{}T_{}-{}-MLR'.format(AOI, int(float(THS)*100), MOI, MOD_SEL)
rf = pkl.load(path.join(PT_OUT, fNameOut+'.pkl'))
###############################################################################
# Sweep-Evaluate Model
###############################################################################
fltr = {
    'i_ren': 25.0,
    'i_res': 50.0,
    'i_rei': 7,
    'i_pct': 1.00, 
    'i_pmd': 1.00, 
    'i_mfr': 0.00, 
    'i_mtf': 0.75,
    'i_fvb': 0.00
}
# [fltr.pop(i) for i in HD_IND]
# kSweep = ['i_fvb', 'i_mfr']
# sweep = np.arange(0, .5, .01)
probe = (
    ('ren', fltr['i_ren']), ('rer', fltr['i_res']), ('rei', fltr['i_rei']),
    ('pct', fltr['i_pct']), ('pmd', fltr['i_pmd']),
    ('mfr', fltr['i_mfr']), ('mtf', fltr['i_mtf']), ('fvb', fltr['i_fvb'])
)
vct = np.array([[i[1] for i in probe]])
rf.predict(vct)[0]