
import sys
from os import path
from re import match
from glob import glob
from joblib import dump, load
from datetime import datetime
import pandas as pd
import MoNeT_MGDrivE as monet
import tGD_aux as aux
import tGD_gene as drv
from more_itertools import locate
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

if monet.isNotebook():
    (USR, AOI, DRV, QNT, THS, NME, TRC) = (
        'srv', 'HLT', 'linkedDrive', '50', '0.1', 'NM', 'HLT'
    )
else:
    (USR, AOI, DRV, QNT, THS, NME, TRC) = sys.argv[1:]
exp = aux.EXPS[0]
# Filename --------------------------------------------------------------------
if NME == 'BD':
    FNAME = 'DTA_FLTR_BD.csv'
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
(drive, land) = (drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE), [[0], ])
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, '100', 'SUMMARY')
# Time and head --------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_OUT, tS,
    '{} DtaConvert [{}:{}:{}:{}]'.format('tGD', DRV, QNT, AOI, THS)
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
for ix in range(expsNum):
    print('{}* Processing: {}/{}{}'.format(CBBL, ix+1, expsNum, CEND), end='\r')
    row = DATA.iloc[ix]
    i=0
    ins = [str(int(row[i]*zipper[i][0])).zfill(zipper[i][1]) for i in zipper]
    fname = aux.XP_NPAT.format(*ins[:], TRC, '00', 'srp', 'bz')
    prePath = PT_PRE.split('/')
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

