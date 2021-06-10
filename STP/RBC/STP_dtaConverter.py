
import sys
from os import path
from re import match
from glob import glob
from joblib import dump, load
from datetime import datetime
import pandas as pd
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
from more_itertools import locate
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

if monet.isNotebook():
    (USR, LND, AOI, QNT) = ('dsk', 'PAN', 'HLT', '50')
else:
    (USR, LND, AOI, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    )
FNAME = 'DTA_FLTR.csv'
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
###############################################################################
# Paths
###############################################################################
EXPS = aux.getExps(LND)
(drive, land) = (
    drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND)
)
(PT_ROT, _, _, PT_PRE, _, _) = aux.selectPath(USR, EXPS[0], LND)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
# Time and head --------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_OUT, tS,
    '{} DtaConvert [{}:{}:{}:{}]'.format(aux.XP_ID, aux.DRV, QNT, AOI, aux.THS)
)
###############################################################################
# Read CSV
###############################################################################
thsStr = str(int(float(aux.THS)*100))
(fName_I, fName_R, fName_C) = (
    'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'REG_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'CLS_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr)
)
DATA = pd.read_csv(path.join(PT_OUT, FNAME))
expsNum = DATA.shape[0]
###############################################################################
# Transform Entries
###############################################################################
(SCA, PAD) = (aux.DATA_SCA, aux.DATA_PAD)
catSorting = [i for i in list(DATA.columns) if i[0]=='i']
outSorting = [i for i in list(DATA.columns) if i[0]!='i']
zipper = {i: (SCA[i], PAD[i]) for i in catSorting}
# Transform to fnames ---------------------------------------------------------
expsIter = [None]*expsNum
for ix in range(expsNum):
    row = DATA.iloc[ix]
    ins = [str(int(row[i]*zipper[i][0])).zfill(zipper[i][1]) for i in zipper]
    (mig, grp) = (ins[-1], ins[-2])
    fname = aux.XP_PTRN.format(*ins[:-2], 'HLT', ins[-2], 'srp', 'bz')
    (tti, tto, wop, poe, _, cpt) = [row[i] for i in outSorting]
    expsIter[ix] = (
        ix, path.join(PT_PRE, fname), 
        tti, tto, wop, 0, 0, poe, cpt
    )
###############################################################################
# Export iter
###############################################################################
dump(expsIter, path.join(PT_OUT, 'DTA_PST.job'))
