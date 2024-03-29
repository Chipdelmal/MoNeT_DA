

import sys
from glob import glob
from datetime import datetime
from os import path
from re import match
import numpy as np
import pandas as pd
from functools import reduce
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd


if monet.isNotebook():
    (USR, LND, AOI, DRV, QNT) = ('lab', 'SPA', 'HLT', 'LDR', '50')
else:
    (USR, LND, AOI, DRV, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], 
        sys.argv[4], sys.argv[5]
    )
EXPS = aux.getExps(LND)
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
###############################################################################
# Paths
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND, USR=USR)
)
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND, DRV)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
# Time and head --------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_OUT, tS, 
    '{} ClsUnify [{}:{}:{}:{}]'.format(DRV, DRV, QNT, AOI, aux.THS)
)
###############################################################################
# Merge Dataframes
###############################################################################
dataFrames = []
mtr = 'MNX'
for mtr in ['TTI', 'TTO', 'WOP']:
    print(monet.CBBL+'* Processing {}'.format(mtr)+monet.CEND, end='\r')
    pth = path.join(PT_OUT, 'SCA_{}_{}_{}_qnt.csv'.format(AOI, mtr, QNT))
    dta = pd.read_csv(pth)
    dataCols = [k for k in dta.columns if k[0]=='i']+[aux.THS]
    dta = dta[dataCols]
    dta = dta.rename(columns={aux.THS: mtr})
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
fNameOut = 'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, int(float(aux.THS)*100))
fullDataframe.to_csv(path.join(PT_OUT, fNameOut), index=False)
