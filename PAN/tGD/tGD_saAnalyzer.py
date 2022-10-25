
import math
from os import sys
from os import path
import numpy as np
import pandas as pd
import compress_pickle as pkl
from SALib.analyze import delta, pawn, rbd_fast, hdmr
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
# import squarify
import tGD_aux as aux
import tGD_gene as drv
from collections import Counter
from more_itertools import locate


if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'tGD', '50', 'HLT', '0.1', 'CPT')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
exp = '100'
###############################################################################
# Setting Paths Up and Reading SA Constants
###############################################################################
(SAMPLES_NUM, VARS_RANGES) = (aux.SA_SAMPLES, aux.SA_RANGES)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    [[0], ]
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_ROT = "/".join(PT_ROT.split("/")[:-2])
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
###############################################################################
# Read SA Files
###############################################################################
# (PROBLEM, SAMPLER, EXP) = (
#     pkl.load(path.join(PT_MTR, 'SA_experiment.pkl')),
#     np.load(path.join(PT_MTR, 'SA_experiment.npy')),
#     pd.read_csv (path.join(PT_MTR, 'SA_experiment.csv'))
# )
###############################################################################
# Read Results CSV
###############################################################################
thsStr = str(int(float(THS)*100))
(fName_I, fName_R, fName_C) = (
    'SCA_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'REG_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr),
    'CLS_{}_{}Q_{}T.csv'.format(AOI, QNT, thsStr)
)
RES = pd.read_csv(path.join(PT_OUT, fName_I))
###############################################################################
# Explore
###############################################################################
headerInd = list(RES.columns)
uqVal = {i: len(list(RES[i].unique())) for i in headerInd}
resNum = RES.shape
###############################################################################
# Read SA Files
###############################################################################
(PROBLEM, SAMPLER, EXP) = (
    pkl.load(path.join(PT_MTR, 'SA_experiment.pkl')),
    np.load(path.join(PT_MTR, 'SA_experiment.npy')),
    pd.read_csv (path.join(PT_MTR, 'SA_experiment.csv'))
)
###############################################################################
# Assemble Output Vector
###############################################################################
headExp = list(RES.columns)
headRes = [i for i in RES.columns if i[0]=='i']
saVars = set([i[0] for i in ([i for i in VARS_RANGES if (len(i[1])>1)])])
saCnst = set([i[0] for i in ([i for i in VARS_RANGES if (len(i[1])<=1)])])
rsnst = set([i.split('_')[-1] for i in headRes]) - set(PROBLEM['names'])
# Generate filter -------------------------------------------------------------
# ix = 70
(FEATS, LABLS) = (
    [i for i in headerInd if i[0]=='i'], 
    [i for i in headerInd if i[0]!='i']
)
FEATS = [i for i in FEATS if uqVal[i]>1]
bounds = [(min(RES[i]), max(RES[i])) for i in FEATS]
problem = {
    'num_vars': len(FEATS),
    'names': FEATS,
    'bounds': bounds,
    'dists': ['unif']*len(FEATS),
    'sample_scaled': True
}
(X, Y) = (np.asarray(RES[FEATS]), np.asarray(RES[MOI]))
print(problem)
###############################################################################
# Run SA
###############################################################################
SA_delta = delta.analyze(PROBLEM, SAMPLER, Y, print_to_console=False)
SA_pawn = pawn.analyze(PROBLEM, SAMPLER, Y, print_to_console=False)
SA_hdmr = hdmr.analyze(PROBLEM, SAMPLER, Y, print_to_console=False)
SA_fast = rbd_fast.analyze(PROBLEM, SAMPLER, Y, print_to_console=False)
# Compile dataframes ----------------------------------------------------------
pawnDF = pd.DataFrame(SA_pawn)
deltaDF = pd.DataFrame(SA_delta)
hdmrDF = pd.DataFrame({'S1': SA_hdmr['ST'], 'S1_conf': SA_hdmr['ST_conf'], 'names': SA_hdmr['names']})
fastDF = pd.DataFrame(SA_fast)
###############################################################################
# Plot SA
###############################################################################
delta = deltaDF[['names', 'delta', 'S1']]
pawn = pawnDF[['names', 'mean', 'median']]
fast = hdmrDF[['names', 'S1']]
hdmr = fastDF.iloc[:len(aux.SA_RANGES)][['names', 'S1']]
# Re-shape --------------------------------------------------------------------
iVar = [i[0] for i in aux.DATA_HEAD[:-1]]
validFeat = [sal[0] for sal in aux.SA_RANGES if (len(sal[1])>1)]
# Assemble dataframe ----------------------------------------------------------
df = pd.DataFrame([
        ['Delta', *aux.getSASortedDF(delta, 'S1', validFeat)], 
        ['PAWN',  *aux.getSASortedDF(pawn, 'median', validFeat)], 
        ['FAST',  *aux.getSASortedDF(fast, 'S1', validFeat)], 
        ['HDMR',  *aux.getSASortedDF(hdmr, 'S1', validFeat)], 
    ],
    columns=['name']+validFeat
)
dfT = df.transpose()
new_header = dfT.iloc[0]
dfT = dfT[1:]
dfT.columns = new_header
dfT = dfT.reset_index()
dfT.sort_values('Delta', ascending=True, inplace=True)
# Barchart --------------------------------------------------------------------
clr = [
    '#FF1A4BAA', '#8338ecAA', '#3a86ffAA', '#00f5d4AA', 
    '#8d99aeAA', '#cdb4dbAA', '#03045eAA'    
]
(fig, ax) = plt.subplots(figsize=(4, 2))
dfT.plot.barh(
    x='index', stacked=False, xlim=(0, 1), ax=ax,
    ylabel='', xlabel='',
    title='', logx=False, color=clr
)
plt.legend(loc='lower right', frameon=False)
plt.savefig(
    path.join(PT_IMG, f'SA-{AOI}_{MOI}-{QNT}_qnt.svg'), 
    format='svg', facecolor='w', bbox_inches='tight', 
    pad_inches=0.1, dpi=300, transparent=False
)
###############################################################################
# Export to Disk
###############################################################################
outPairs = list(zip(
    ['Delta', 'PAWN', 'HDMR', 'FAST'],
    [deltaDF, pawnDF, hdmrDF, fastDF],
    [SA_delta, SA_pawn, SA_hdmr, SA_fast]
))
for (name, df, dct) in outPairs:
    fName = path.join(PT_MTR, f'SA-{AOI}_{MOI}-{name}-{QNT}_qnt')
    df.to_csv(fName+'.csv', index=False)
    pkl.dump(dct, fName+'.pkl')

