
import math
from os import sys
from os import path
import numpy as np
import pandas as pd
import compress_pickle as pkl
from SALib.analyze import sobol, delta, pawn, rbd_fast, hdmr
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import squarify
import FMS_aux as aux
import FMS_gene as drv


if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'PGS', '50', 'HLT', '0.1', 'CPT')
else:
    (USR, DRV, QNT, AOI, THS, MOI) = sys.argv[1:]
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
###############################################################################
# Read SA Files
###############################################################################
(PROBLEM, SAMPLER, EXP) = (
    pkl.load(path.join(PT_MTR, 'SA_experiment.pkl')),
    np.load(path.join(PT_MTR, 'SA_experiment.npy')),
    pd.read_csv (path.join(PT_MTR, 'SA_experiment.csv'))
)
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
RES.shape
###############################################################################
# Assemble Output Vector
###############################################################################
headExp = list(EXP.columns)
headRes = [i for i in RES.columns if i[0]=='i']
saVars = set([i[0] for i in ([i for i in VARS_RANGES if (len(i[1])>1)])])
saCnst = set([i[0] for i in ([i for i in VARS_RANGES if (len(i[1])<=1)])])
rsnst = set([i.split('_')[-1] for i in headRes]) - set(PROBLEM['names'])
# Generate filter -------------------------------------------------------------
# ix = 70
expNum = EXP.shape[0]
(matchesSizes, outVector) = ([0]*expNum, np.zeros(expNum))
for ix in range(expNum):
    print('Processing {:06d}/{:06d}'.format(ix+1, expNum), end='\r')
    rowVals = EXP.iloc[ix].to_dict()
    # Fix discrepancy in release size
    rowVals['res'] = round(rowVals['rer'], 2)
    rowVals.pop('rer')
    # Add group id to filter
    rowVals['grp'] = 0
    # Assemble the filter
    fltr = {f'i_{k}': v for k, v in rowVals.items()}
    # Filter Results for entry ------------------------------------------------
    ks = list(fltr.keys())
    ks.remove('i_res')
    rowFilterMtx = [np.isclose(RES[k], fltr[k], atol=1e-4) for k in ks]
    boolFilter = [all(i) for i in zip(*rowFilterMtx)]
    boolFilterRes = np.isclose(RES['i_res'], fltr['i_res'], atol=1e-1)
    boolFull = [a and b for (a, b) in zip(boolFilterRes, boolFilter)]
    dataRow = RES[boolFull]
    (matchesSizes[ix], outVector[ix]) = (dataRow.shape[0], float(dataRow[MOI]))
if len(set(matchesSizes))>1:
    print("Error in the output vector!")
    # matchesSizes.index(0)
###############################################################################
# Run SA
###############################################################################
# SA_sobol = sobol.analyze(PROBLEM, outVector, print_to_console=True)
SA_delta = delta.analyze(PROBLEM, SAMPLER, outVector, print_to_console=True)
SA_pawn = pawn.analyze(PROBLEM, SAMPLER, outVector, print_to_console=True)
SA_hdmr = hdmr.analyze(PROBLEM, SAMPLER, outVector, print_to_console=True)
SA_fast = rbd_fast.analyze(PROBLEM, SAMPLER, outVector, print_to_console=True)
# Compile dataframes ----------------------------------------------------------
pawnDF = pd.DataFrame(SA_pawn)
# sobolOut = list(zip(
#     SA_sobol['S1'], SA_sobol['S1_conf'], 
#     SA_sobol['ST'], SA_sobol['ST_conf'],
#     pawnDF['names']
# ))
# sobolDF = pd.DataFrame(sobolOut, columns=['S1', 'S1_conf', 'ST', 'ST_conf', 'names'])
deltaDF = pd.DataFrame(SA_delta)
hdmrDF = pd.DataFrame({'S1': SA_hdmr['ST'], 'S1_conf': SA_hdmr['ST_conf'], 'names': SA_hdmr['names']})
fastDF = pd.DataFrame(SA_fast)
fastDF = pd.DataFrame(SA_fast)
###############################################################################
# Plots
###############################################################################
methods = list(zip(
    ("FAST", "Delta", "PAWN", "HDMR"), #, "Sobol"), 
    (fastDF, deltaDF, pawnDF, hdmrDF) #, sobolDF)
))
mIx = 1
for mIx in range(len(methods)):
    (method, saRes) = methods[mIx]
    tag = ('S1' if  method is not 'PAWN' else 'median')
    fltr = [not (math.isnan(i)) for i in saRes[tag]]
    (sizes, label) = (
        abs(saRes[tag][fltr]), 
        [i.split('_')[-1] for i in saRes['names'][fltr]]
    )
    lbl = ['{}\n{:.2f}'.format(a, b) for (a, b) in zip(label, sizes)]
    (fig, ax) = plt.subplots(figsize=(5,5))
    squarify.plot(sizes=sizes, label=lbl, alpha=0.5, color=aux.TREE_COLS)
    ax.set_aspect(1)
    plt.axis('off')
    fig.savefig(
        path.join(PT_MTR, f'SA-{AOI}_{MOI}-{method}-{QNT}_qnt'+'.png'), 
        dpi=500, bbox_inches='tight', transparent=True
    )
###############################################################################
# Export to Disk
###############################################################################
outPairs = list(zip(
    ['Delta', 'PAWN', 'HDMR', 'FAST'], #, 'Sobol']
    [deltaDF, pawnDF, hdmrDF, fastDF], #, sobolDF] 
    [SA_delta, SA_pawn, SA_hdmr, SA_fast] #, SA_sobol]
))
for (name, df, dct) in outPairs:
    fName = path.join(PT_MTR, f'SA-{AOI}_{MOI}-{name}-{QNT}_qnt')
    df.to_csv(fName+'.csv', index=False)
    pkl.dump(dct, fName+'.pkl')

