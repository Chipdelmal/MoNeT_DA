
import sys
from glob import glob
from datetime import datetime
from os import path
from re import match
import numpy as np
import pandas as pd
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import tGD_aux as aux
import tGD_gene as drv


if monet.isNotebook():
    (USR, DRV, AOI, QNT, MTR, THS) = ('srv', 'linkedDrive', 'HLT', '50', 'WOP', '0.1')
else:
    (USR, DRV, AOI, THS) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
exp = aux.EXPS[0]
###########################################################################
# Paths
###########################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    [[0], ]
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_OUT = path.join(PT_ROT, 'ML')
PT_OUT_ML = PT_OUT.replace('/100', '')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
# Time and head -----------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_OUT, tS, 
    '{} ClsUnifyML [{}:{}]'.format(DRV, AOI, THS)
)
###############################################################################
# Merge Dataframes
###############################################################################
for fid in ('SCA', 'REG'):
    dataFrames = []
    mtr = 'MNX'
    for mtr in ['TTI', 'TTO', 'WOP']:
        print(monet.CBBL+'* Processing {}'.format(mtr)+monet.CEND, end='\r')
        pth = path.join(PT_OUT, '{}_{}_{}_MLR.csv'.format(fid, AOI, mtr))
        dta = pd.read_csv(pth)
        dataCols = [k for k in dta.columns if k[0]=='i']+[THS]
        dta = dta[dataCols]
        dta = dta.rename(columns={THS: mtr})
        dataFrames.append(dta)
    for mtr in ['CPT', ]:
        print(monet.CBBL+'* Processing {}'.format(mtr)+monet.CEND, end='\r')
        pth = path.join(PT_OUT, '{}_{}_{}_MLR.csv'.format(fid, AOI, mtr))
        dta = pd.read_csv(pth)
        dataFrames.append(dta)
    for mtr in ['MNX', ]:
        print(monet.CBBL+'* Processing {}'.format(mtr)+monet.CEND, end='\r')
        pth = path.join(PT_OUT, '{}_{}_{}_MLR.csv'.format(fid, AOI, mtr))
        dta = pd.read_csv(pth)
        dataCols = [k for k in dta.columns if k[0]=='i']+['min']
        dta = dta[dataCols]
        dta = dta.rename(columns={'min': 'MNF'})
        dataFrames.append(dta)
    print(monet.CBBL+'* Reducing Dataframes {}'.format(mtr)+monet.CEND, end='\r')
    indVars = [i[0] for i in aux.DATA_HEAD]
    for (i, mtr) in enumerate(('TTO', 'WOP', 'CPT', 'MNF')):
        dataFrames[0][mtr] = dataFrames[i+1][mtr]
    fullDataframe = dataFrames[0]
    ###########################################################################
    # Export
    ###########################################################################
    fNameOut = '{}_{}_{}T_MLR.csv'.format(fid, AOI, int(float(THS)*100))
    fullDataframe.to_csv(path.join(PT_OUT_ML, fNameOut), index=False)
