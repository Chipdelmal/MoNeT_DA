
import sys
from os import path
from numpy import full
import pandas as pd
from functools import reduce
from datetime import datetime
import MoNeT_MGDrivE as monet
import TPP_aux as aux
import TPP_gene as drv

if monet.isNotebook():
    (USR, LND, EXP, DRV, AOI, QNT, THS) = (
        'zelda', 'BurkinaFaso', 'highEIR', 'HUM', 'CSS', '50', '0.1'
    )
else:
    (USR, LND, EXP, DRV, AOI, QNT, THS) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
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
    PT_ROT, PT_OUT, tS, 
    '{} ClsUnify [{}:{}:{}]'.format(DRV, QNT, AOI, THS)
)
###############################################################################
# Merge Dataframes
###############################################################################
for fid in ('SCA', 'REG'):
    dataFrames = []
    mtr = 'MNX'
    for mtr in ['TTI', 'TTO', 'WOP']:
        print(monet.CBBL+'* Processing {}'.format(mtr)+monet.CEND, end='\r')
        pth = path.join(PT_OUT, '{}_{}_{}_{}_qnt.csv'.format(fid, AOI, mtr, QNT))
        dta = pd.read_csv(pth)
        dataCols = [k for k in dta.columns if k[0]=='i']+[THS]
        dta = dta[dataCols]
        dta = dta.rename(columns={THS: mtr})
        dataFrames.append(dta)
    for mtr in ['POE', 'CPT']:
        print(monet.CBBL+'* Processing {}'.format(mtr)+monet.CEND, end='\r')
        pth = path.join(PT_OUT, '{}_{}_{}_{}_qnt.csv'.format(fid, AOI, mtr, QNT))
        dta = pd.read_csv(pth)
        dataFrames.append(dta)
    for mtr in ['MNX', ]:
        print(monet.CBBL+'* Processing {}'.format(mtr)+monet.CEND, end='\r')
        pth = path.join(PT_OUT, '{}_{}_{}_{}_qnt.csv'.format(fid, AOI, mtr, QNT))
        dta = pd.read_csv(pth)
        dataCols = [k for k in dta.columns if k[0]=='i']+['min']
        dta = dta[dataCols]
        dta = dta.rename(columns={'min': 'MNF'})
        dataFrames.append(dta)
    fullDataframe = reduce(lambda x, y: pd.merge(x, y, ), dataFrames)
    ###########################################################################
    # Add zero-release control values
    ###########################################################################
    # fltr = [fullDataframe['i_ren']==0, fullDataframe['i_res']==0]
    # zeroEntry = fullDataframe[list(map(all, zip(*fltr)))].iloc[0].copy()
    # (ren, res) = [list(fullDataframe[i].unique()) for i in ('i_ren', 'i_res')]
    # for renT in ren:
    #     tmp = zeroEntry.copy()
    #     tmp['i_ren']=renT
    #     tmp['i_res']=0
    #     fullDataframe.loc[-1]=tmp
    #     fullDataframe = fullDataframe.reset_index(drop=True)
    # for resT in res:
    #     tmp = zeroEntry.copy()
    #     tmp['i_ren']=0
    #     tmp['i_res']=resT
    #     fullDataframe.loc[-1]=tmp
    #     fullDataframe = fullDataframe.reset_index(drop=True)
    ###########################################################################
    # Export
    ###########################################################################
    fNameOut = '{}_{}_{}Q_{}T.csv'.format(fid, AOI, QNT, int(float(THS)*100))
    fullDataframe.to_csv(path.join(PT_OUT, fNameOut), index=False)
