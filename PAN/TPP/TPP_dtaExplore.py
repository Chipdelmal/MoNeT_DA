
import sys
from os import path
import pandas as pd
from glob import glob
from joblib import dump
from datetime import datetime
import MoNeT_MGDrivE as monet
import TPP_aux as aux
import TPP_gene as drv

if monet.isNotebook():
    (USR, LND, EXP, DRV, AOI, QNT, THS, TRC) = (
        'zelda', 'Kenya', 'highEIR', 'LDR', 'HLT', '50', '0.1', 'HLT'
    )
else:
    (USR, LND, EXP, DRV, AOI, QNT, THS, TRC) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'zelda':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###########################################################################
# Paths
###########################################################################
(NH, NM) = aux.getPops(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=NM, humSize=0),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, EXP)
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
(DATA, DATA_FILE) = (
    pd.read_csv(path.join(PT_OUT, fName_I)),
    pd.read_csv(path.join(PT_OUT, fName_R))
)
# Features and labels ---------------------------------------------------------
COLS = list(DATA.columns)
(FEATS, LABLS) = (
    [i for i in COLS if i[0]=='i'], [i for i in COLS if i[0]!='i']
)
###############################################################################
# Filter Output with Constraints
###############################################################################
wopRge = (-10*365, 15*365)
fltr = (
    wopRge[0] <= DATA['WOP'],   DATA['WOP']   <= wopRge[1],
)
constrained = DATA[list(map(all, zip(*fltr)))]
constrainedFiles = DATA_FILE[list(map(all, zip(*fltr)))]
###############################################################################
# Export
###############################################################################
print('{}* Found {}/{} matches (Check filter if needed!){}'.format(
	monet.CBBL, constrained.shape[0], DATA.shape[0], monet.CEND
))
constrained.to_csv(path.join(PT_OUT, 'DTA_FLTR.csv'), index=False)
constrainedFiles.to_csv(path.join(PT_OUT, 'DTA_FLTR_Files.csv'), index=False)
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
ix = 1
skipped = 0
for ix in range(expsNum):
    print(
        '{}* Processing: {}/{}{}'.format(monet.CBBL, ix+1, expsNum, monet.CEND), 
        end='\r'
    )
    # row = constrained.iloc[ix]
    row = constrainedFiles.iloc[ix]
    i=0
    ins = [str(int(row[i])).zfill(zipper[i][1]) for i in zipper]
    fname = aux.XP_PTRN.format(*ins[:-1], TRC, '00', 'srp', 'bz') 
    prePath = PT_PRE.split('/')
    fpath = path.join('/'.join(prePath), fname)
    fpath.split('/')[-1]
    if path.isfile(fpath):
        (tti, tto, wop, poe, _, cpt, mnf) = [row[i] for i in outSorting]
        expsIter.append([
            counter, fpath,
            tti, tto, wop, mnf, 0, poe, cpt
        ])
        counter = counter + 1
    else:
        print(fname)
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