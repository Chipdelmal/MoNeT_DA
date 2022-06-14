

import sys
from glob import glob
from datetime import datetime
from os import path
import pandas as pd
from functools import reduce
import MoNeT_MGDrivE as monet
import tGD_aux as aux
import tGD_gene as drv


# print(sys.argv[1:])
if monet.isNotebook():
    (USR, DRV, AOI, QNT, THS) = ('srv1', 'linkedDrive', 'WLD', '50', '0.1')
else:
    (USR, DRV, AOI, QNT, THS) = sys.argv[1:]
EXPS = aux.EXPS
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
exp = EXPS[0]
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
    PT_ROT, PT_OUT, tS, 
    '{} ClsUnify [{}:{}:{}:{}]'.format(DRV, DRV, QNT, AOI, THS)
)
# Revert THS for AOI ---------------------------------------------------------
if AOI == 'TRS':
    THS = str(1-float(THS))
###############################################################################
# Merge Dataframes
###############################################################################
dataFrames = []
mtr = 'MNX'
for mtr in ['TTI', 'TTO', 'WOP']:
    print(monet.CBBL+'* Processing {}'.format(mtr)+monet.CEND, end='\r')
    pth = path.join(PT_OUT, 'SCA_{}_{}_{}_qnt.csv'.format(AOI, mtr, QNT))
    dta = pd.read_csv(pth)
    dataCols = [k for k in dta.columns if k[0]=='i']+[THS]
    dta = dta[dataCols]
    dta = dta.rename(columns={THS: mtr})
    dataFrames.append(dta)
for mtr in ['POE', 'CPT']:
    print(monet.CBBL+'* Processing {}'.format(mtr)+monet.CEND, end='\r')
    pth = path.join(PT_OUT, 'SCA_{}_{}_{}_qnt.csv'.format(AOI, mtr, QNT))
    dta = pd.read_csv(pth)
    dataFrames.append(dta)
for mtr in ['MNX', ]:
    print(monet.CBBL+'* Processing {}'.format(mtr)+monet.CEND, end='\r')
    pth = path.join(PT_OUT, 'SCA_{}_{}_{}_qnt.csv'.format(AOI, mtr, QNT))
    dta = pd.read_csv(pth)
    dataCols = [k for k in dta.columns if k[0]=='i']+['min']
    dta = dta[dataCols]
    dta = dta.rename(columns={'min': 'MNF'})
    dataFrames.append(dta)
fullDataframe = reduce(lambda x, y: pd.merge(x, y, ), dataFrames)
###############################################################################
# Export
###############################################################################
fNameOut = 'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, int(float(THS)*100))
fullDataframe.to_csv(path.join(PT_OUT, fNameOut), index=False)
