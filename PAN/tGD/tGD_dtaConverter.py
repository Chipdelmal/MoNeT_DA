
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
    (USR, DRV, AOI, QNT, THS, NME, TRC) = (
        'srv2', 'tGD', ('HLT', 'TRS'), '50', ('0.25', '0.75'), 'NM', ('HLT', 'TRS')
    )
else:
    (USR, DRV, AOI, QNT, THS, NME, TRC) = sys.argv[1:]
exp = aux.EXPS[0]
# Filename --------------------------------------------------------------------
FNAME = 'DTA_FLTR_{}.csv'
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
(CBBL, CEND) = (monet.CBBL, monet.CEND)
###############################################################################
# Paths
###############################################################################
(drive, land) = (drv.driveSelector(DRV, AOI[0], popSize=aux.POP_SIZE), [[0], ])
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
DATA = [pd.read_csv(path.join(PT_OUT, FNAME.format(i))) for i in AOI]
###############################################################################
# Transform Entries
###############################################################################
(SCA, PAD) = (aux.DATA_SCA, aux.DATA_PAD)
catSorting = [i for i in list(DATA[0].columns) if i[0]=='i']
outSorting = [i for i in list(DATA[0].columns) if i[0]!='i']
zipper = {i: (int(SCA[i]), PAD[i]) for i in catSorting}
# print(outSorting)
# Transform to fnames ---------------------------------------------------------
expsNum = DATA[0].shape[0]
(expsIter, skipped, counter) = ([], 0, 0)
ix = 2
# Check for padding!!!!!!!!!!! (inconsistent) ---------------------------------
for ix in range(expsNum):
    print('{}* Processing: {}/{}{}'.format(CBBL, ix+1, expsNum, CEND), end='\r')
    rows = [dta.iloc[ix] for dta in DATA]
    i=0
    ins = [str(int(rows[0][i]*zipper[i][0])).zfill(zipper[i][1]) for i in zipper]
    fnames = [aux.XP_NPAT.format(*ins[:], trc, '00', 'srp', 'bz') for trc in TRC]
    prePath = PT_PRE.split('/')
    fpaths = [path.join('/'.join(prePath), fname) for fname in fnames]
    if path.isfile(fpaths[0]) and path.isfile(fpaths[1]):
        for (fpath, row) in zip(fpaths, rows):
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

