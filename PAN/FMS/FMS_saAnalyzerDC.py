
import math
from os import sys
from os import path
import numpy as np
import pandas as pd
import compress_pickle as pkl
from SALib.analyze import rbd_fast, delta, pawn, hdmr
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
###############################################################################
# Run SA
###############################################################################
SA_delta = delta.analyze(problem, X, Y, print_to_console=True)
SA_pawn = pawn.analyze(problem, X, Y, print_to_console=True)
SA_hdmr = hdmr.analyze(problem, X, Y, print_to_console=True)
SA_fast = rbd_fast.analyze(problem, X, Y, print_to_console=True)
# Compile dataframes ----------------------------------------------------------
deltaDF = pd.DataFrame(SA_delta)
pawnDF = pd.DataFrame(SA_pawn)
hdmrDF = pd.DataFrame({'S1': SA_hdmr['ST'], 'S1_conf': SA_hdmr['ST_conf'], 'names': SA_hdmr['names']})
fastDF = pd.DataFrame(SA_fast)
###############################################################################
# Plots
###############################################################################
methods = list(zip(
    ("FAST", "Delta", "PAWN", "HDMR"), 
    (fastDF, deltaDF, pawnDF, hdmrDF)
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
# # Stacked bars ----------------------------------------------------------------
# width=.35
# cats = [i.split('_')[-1] for i in saRes['names'][fltr]]
# methods = ("FAST", "Delta", "PAWN", "HDMR")
# dfs = (deltaDF, pawnDF, hdmrDF, fastDF)
# (fig, ax) = plt.subplots()
# ax.bar(cats, deltaDF['S1'], width, label='Delta')
# ax.bar(cats, fastDF['S1'], width, label='FAST')
# ax.bar(cats, pawnDF['median'], width,label='PAWN')
# ax.bar(cats, hdmrDF['S1'][[i in set(deltaDF['names']) for i in list(hdmrDF['names'])]], width,label='HDMR')
# ax.legend()
# plt.show()
# # Stacked bars ----------------------------------------------------------------
# sArray = np.asarray([
#     fastDF['S1'], deltaDF['S1'], pawnDF['median'],
#     hdmrDF['S1'][[i in set(deltaDF['names']) for i in list(hdmrDF['names'])]]
# ])
# row_sums = sArray.sum(axis=1)
# sNorm = sArray/row_sums[:, np.newaxis]
# (fig, ax) = plt.subplots()
# for i in range(len(cats)):
#     ax.bar(methods, sArray[:,i], width, label=cats[i])
# ax.legend()
# plt.show()
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