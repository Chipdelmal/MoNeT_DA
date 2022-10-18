
import sys
from os import path
import pandas as pd
from glob import glob
from joblib import dump
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import CEF_aux as aux
import CEF_gene as drv
import warnings
warnings.filterwarnings("ignore")

if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS) = ('srv', 'PGS', '50', 'HLT', '0.1')
else:
    (USR, DRV, QNT, AOI, THS) = sys.argv[1:]
TRACE_NUM = aux.SA_SAMPLES
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###########################################################################
# Paths
###########################################################################
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
# Time and head -----------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_IMG, tS, 
    '{} DtaDICE [{}:{}:{}:{}]'.format('FMS', DRV, QNT, AOI, THS)
)
###############################################################################
# Read CSV
###############################################################################
thsStr = str(int(float(THS)*100))
(fName_I, fName_R, fName_C) = (
    'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'REG_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'CLS_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr)
)
DATA = pd.read_csv(path.join(PT_OUT, fName_I))
# Features and labels ---------------------------------------------------------
COLS = list(DATA.columns)
(FEATS, LABLS) = (
    [i for i in COLS if i[0]=='i'], [i for i in COLS if i[0]!='i']
)
###############################################################################
# DICE Plot
###############################################################################
(sampleRate, shuffle) = (TRACE_NUM/DATA.shape[0], True)
(pFeats, ans) = (aux.pFeats, aux.DICE_PARS)
# Filter dataset on specific features (drop others) ---------------------------
dataEffect = DATA[
    (DATA['i_ren'] > 0) & (DATA['i_res'] > 0) & (DATA['i_grp'] == 0)
]
# Select rows to highlight on constraints ------------------------------------
# dataHighlight = DATA[
#     ((DATA['i_rsg'] + DATA['i_gsv']) > 1e-5) & 
#     (DATA['i_fch'] > .8) & (DATA['i_fcr'] > .8)
# ]
highRows = set([]) # set(dataHighlight.index)
###############################################################################
# Iterate through AOI
###############################################################################
(yVar, sigma, col, yRange) = ans[0]
for (yVar, sigma, col, yRange) in ans[:]:
    Parallel(n_jobs=JOB)(
        delayed(aux.exportDICEParallel)(
            AOI, xVar, yVar, dataEffect, FEATS, PT_IMG, hRows=highRows,
            dpi=400, scale=scale, wiggle=True, sd=sigma, sampleRate=sampleRate,
            color=col, hcolor='#000000'+'50', lw=0.5, hlw=0.1, yRange=yRange,
            ticksHide=False
        ) for (xVar, scale) in pFeats
    )