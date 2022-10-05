
import math
from os import sys
from os import path
import numpy as np
import pandas as pd
import compress_pickle as pkl
from SALib.analyze import sobol, delta, pawn, rbd_fast, hdmr
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
# import squarify
import PGS_aux as aux
import PGS_gene as drv


if monet.isNotebook():
    (USR, DRV, QNT, AOI, THS, MOI) = ('srv', 'PGS', '50', 'HLT', '0.1', 'WOP')
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
###############################################################################
# Reading SA Exported files
###############################################################################
name = SA_NAMES[-1]
resultsSA = {}
for name in SA_NAMES:
    fName = path.join(PT_MTR, f'SA-{AOI}_{MOI}-{name}-{QNT}_qnt.csv')
    resultsSA[name] = pd.read_csv(fName)
###############################################################################
# Selecting sensitivities
###############################################################################
delta = resultsSA['Delta'][['names', 'delta', 'S1']]
pawn = resultsSA['PAWN'][['names', 'mean', 'median']]
fast = resultsSA['FAST'][['names', 'S1']]
hdmr = resultsSA['HDMR'].iloc[:len(aux.SA_RANGES)][['names', 'S1']]
###############################################################################
# Reshapping
###############################################################################
iVars = [i[0] for i in aux.SA_RANGES]
labels = list(delta['names'])
df = pd.DataFrame([
        ['Delta', *(delta['S1']/sum(delta['S1']))], 
        ['PAWN',  *(pawn['mean']/sum(pawn['mean']))], 
        ['FAST',  *(fast['S1']/sum(fast['S1']))],
        ['HDMR',  *(hdmr['S1']/sum(hdmr['S1']))],
    ],
    columns=['name']+labels
)
dfT = df.transpose()
new_header = dfT.iloc[0]
dfT = dfT[1:]
dfT.columns = new_header
dfT = dfT.reset_index()
###############################################################################
# Plotting
###############################################################################
dfT.plot.barh(
    x='index',
    stacked=False,
    title='SA'
)