
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
warnings.filterwarnings("ignore", category=UserWarning)

if monet.isNotebook():
    (USR, LND, AOI, DRV, QNT, NME, TRC) = (
        'srv', 'PAN', 'HLT',
        'SDR', '50', 'FC', 
        'HLT'
    )
else:
    (USR, LND, AOI, DRV, QNT, NME, TRC) = (
        sys.argv[1], sys.argv[2], sys.argv[3], 
	    sys.argv[4], sys.argv[5], sys.argv[6], 
        sys.argv[7]
    )
# Filename --------------------------------------------------------------------
if NME == 'SX':
    FNAME = 'DTA_FLTR_SX.csv'
elif NME == 'BD':
    FNAME = 'DTA_FLTR_BD.csv'
elif NME == 'FC':
    FNAME = 'DTA_FLTR_FC.csv'
else:
    FNAME = 'DTA_FLTR.csv'
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
(CBBL, CEND) = (monet.CBBL, monet.CEND)
###############################################################################
# Paths
###############################################################################
EXPS = aux.getExps(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND, USR=USR)
)
(PT_ROT, _, _, PT_PRE, _, _) = aux.selectPath(USR, EXPS[0], LND, DRV)
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
# print(outSorting)
# Transform to fnames ---------------------------------------------------------
(expsIter, skipped, counter) = ([], 0, 0)
ix = 2
# Check for padding!!!!!!!!!!! (inconsistent) ---------------------------------
if LND=='PAN':
    zipper['i_grp'] = (zipper['i_grp'][0], 2)
for ix in range(expsNum):
    print('{}* Processing: {}/{}{}'.format(CBBL, ix+1, expsNum, CEND), end='\r')
    row = DATA.iloc[ix]
    i=0
    ins = [
        row[i] if row[i] in aux.SPA_EXP
        else str(int(row[i]*zipper[i][0])).zfill(zipper[i][1])
        for i in zipper
    ]
    (mig, grp) = (ins[-1], ins[-2])
    fname = aux.XP_PTRN.format(*ins[:-2], TRC, ins[-2], 'srp', 'bz')
    prePath = PT_PRE.split('/')
    prePath[-3] = mig
    fpath = path.join('/'.join(prePath), fname)
    if path.isfile(fpath):
        (tti, tto, wop, poe, _, cpt, mnf) = [row[i] for i in outSorting]
        expsIter.append([
            counter, fpath,
            tti, tto, wop, mnf, 0, poe, cpt
        ])
        counter = counter + 1
    else:
        print(fpath)
        skipped = skipped + 1
print('{}* Skipped (no PRE): {}/{}{}'.format(CBBL, skipped, expsNum, CEND))
###############################################################################
# Export iter
###############################################################################
dump(expsIter, path.join(PT_OUT, 'DTA_PST.job'))


