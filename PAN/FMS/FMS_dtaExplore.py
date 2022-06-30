
import sys
from os import path
import pandas as pd
from glob import glob
from joblib import dump
from datetime import datetime
import MoNeT_MGDrivE as monet
import FMS_aux as aux
import FMS_gene as drv

if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, TRC) = ('srv', 'PGS', '50', 'HLT', '0.1', 'HLT')
else:
    (USR, DRV, QNT, AOI, THS, TRC) = sys.argv[1:]
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
    PT_ROT, PT_SUMS, tS, 
    '{} DtaExplore [{}:{}:{}:{}]'.format('FMS', DRV, QNT, AOI, THS)
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
# Filter Output with Constraints
###############################################################################
(renRge, resRge) = ((-1, 20), (-1, 50))
wopRge = (.1*365, 4*365)
fltr = (
    renRge[0] <= DATA['i_ren'], DATA['i_ren'] <= renRge[1],
    resRge[0] <= DATA['i_res'], DATA['i_res'] <= resRge[1],
    wopRge[0] <= DATA['WOP'],   DATA['WOP']   <= wopRge[1],
)
constrained = DATA[list(map(all, zip(*fltr)))]
###############################################################################
# Export
###############################################################################
print('{}* Found {}/{} matches (Check filter if needed!){}'.format(
	monet.CBBL, constrained.shape[0], DATA.shape[0], monet.CEND
))
constrained.to_csv(path.join(PT_OUT, 'DTA_FLTR.csv'), index=False)
###############################################################################
# Transform Entries
###############################################################################
(SCA, PAD) = (aux.DATA_SCA, aux.DATA_PAD)
catSorting = [i for i in list(DATA.columns) if i[0]=='i']
outSorting = [i for i in list(DATA.columns) if i[0]!='i']
zipper = {i: (int(SCA[i]), PAD[i]) for i in catSorting}
# print(outSorting)
# Transform to fnames ---------------------------------------------------------
expsNum = constrained.shape[0]
(expsIter, skipped, counter) = ([[], []], 0, 0)
ix = 2
skipped = 0
for ix in range(expsNum):
    print(
        '{}* Processing: {}/{}{}'.format(monet.CBBL, ix+1, expsNum, monet.CEND), 
        end='\r'
    )
    row = constrained.iloc[ix]
    i=0
    ins = [str(int(row[i]*zipper[i][0])).zfill(zipper[i][1]) for i in zipper]
    fname = aux.XP_PTRN.format(*ins[:-1], TRC, '00', 'srp', 'bz') 
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
        # print(fpath)
        skipped = skipped + 1
print(
    '{}* Skipped (no PRE): {}/{}{}'.format(
        monet.CBBL, skipped, expsNum, monet.CEND
    )
)
###############################################################################
# Export iter
###############################################################################
dump(expsIter, path.join(PT_OUT, 'DTA_PST_{}.job'.format(AOI)))