
import math
from os import sys
from os import path
import numpy as np
import pandas as pd
from datetime import datetime
import compress_pickle as pkl
from SALib.analyze import sobol, delta, pawn, rbd_fast, hdmr
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
# import squarify
import FMS_aux as aux
import FMS_gene as drv


if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'FMS5', '50', 'HLT', '0.1', 'WOP')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
SA_NAMES = ['Delta', 'PAWN', 'HDMR', 'FAST']
###############################################################################
# Setting Paths Up and Reading SA Constants
###############################################################################
(SAMPLES_NUM, VARS_RANGES) = (aux.SA_SAMPLES, aux.SA_RANGES)
(drive, land) = (
    drv.driveSelector(DRV, 'HLT', popSize=aux.POP_SIZE), 
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
    PT_ROT, PT_OUT, tS, 
    '{} SA Plotter [{}:{}:{}]'.format(DRV, AOI, THS, MOI)
)
###############################################################################
# Reading SA Exported files
###############################################################################
name = SA_NAMES[-1]
resultsSA = {}
for name in SA_NAMES:
    fName = path.join(PT_MTR, f'SA-{AOI}_{MOI}-{name}-{QNT}_qnt.csv')
    resultsSA[name] = pd.read_csv(fName)
###############################################################################
# Reading ML Exported files
###############################################################################
fNameOut = '{}_{}T_{}-MLR.png'.format(AOI, int(float(THS)*100), MOI)
impSci = pd.read_csv(path.join(PT_OUT, fNameOut[:-4]+'_PMI-SCI.csv'))
impRfi = pd.read_csv(path.join(PT_OUT, fNameOut[:-4]+'_PMI-RFI.csv'))
shpImp = pd.read_csv(path.join(PT_OUT, fNameOut[:-4]+'_SHP-SHP.csv'))
###############################################################################
# Selecting sensitivities
###############################################################################
delta = resultsSA['Delta'][['names', 'delta', 'S1']]
pawn = resultsSA['PAWN'][['names', 'mean', 'median']]
fast = resultsSA['FAST'][['names', 'S1']]
hdmr = resultsSA['HDMR'].iloc[:len(aux.SA_RANGES)][['names', 'S1']]
isci = impSci[['names', 'mean']]
irfi = impRfi[['Feature', 'Importance']]
shp = shpImp[['names', 'mean']]
###############################################################################
# Reshapping
###############################################################################
iVar = [i[0] for i in aux.DATA_HEAD[:-1]]
validFeat = [sal[0] for sal in aux.SA_RANGES if (len(sal[1])>1)]
# Assemble dataframe ---------------------------------------------------------
df = pd.DataFrame([
        ['Delta', *aux.getSASortedDF(delta, 'S1', validFeat)], 
        # ['PAWN',  *aux.getSASortedDF(pawn, 'mean', validFeat)], 
        ['FAST',  *aux.getSASortedDF(fast, 'S1', validFeat)], 
        ['HDMR',  *aux.getSASortedDF(hdmr, 'S1', validFeat)], 
        ['ISCI',  *aux.getSASortedDF(isci, 'mean', validFeat)], 
        ['IRFI',  *aux.getSASortedDF(irfi, 'Importance', validFeat)], 
        ['SHAP',  *aux.getSASortedDF(shp, 'mean', validFeat)], 
    ],
    columns=['name']+validFeat
)
dfT = df.transpose()
new_header = dfT.iloc[0]
dfT = dfT[1:]
dfT.columns = new_header
dfT = dfT.reset_index()
dfT.sort_values('SHAP', ascending=True, inplace=True)
###############################################################################
# Plotting
###############################################################################
clr = [
    '#FF1A4BAA', '#8338ecAA', '#3a86ffAA', '#00f5d4AA', 
    '#8d99aeAA', '#cdb4dbAA', '#03045eAA'    
]
(fig, ax) = plt.subplots(figsize=(4, 2.75))
dfT.plot.barh(
    x='index', stacked=False, xlim=(0, 1), ax=ax,
    ylabel='', xlabel='',
    title='', logx=False, color=clr
)
plt.legend(loc='lower right')
plt.savefig(
    path.join(PT_IMG, fNameOut[:-4]+'-FIMP.png'), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
(fig, ax) = plt.subplots(figsize=(4, 2.75))
dfT.plot.barh(
    x='index', stacked=False, xlim=(1e-3, 1), ax=ax,
    ylabel='', xlabel='',
    title='', logx=True, color=clr
)
plt.legend(loc='lower right')
plt.savefig(
    path.join(PT_IMG, fNameOut[:-4]+'-FIMP_Log.png'), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
