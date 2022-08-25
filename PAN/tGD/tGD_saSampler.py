
from os import sys
from os import path
import numpy as np
import pandas as pd
import compress_pickle as pkl
from SALib.sample import saltelli
import MoNeT_MGDrivE as monet
import tGD_aux as aux


if monet.isNotebook():
    (USR, DRV) = ('srv2', 'linkedDrive')
else:
    (USR, DRV) = sys.argv[1:]
exp = '100'
###############################################################################
# Setting Paths Up and Reading SA Constants
###############################################################################
(SAMPLES_NUM, VARS_RANGES) = (aux.SA_SAMPLES, aux.SA_RANGES)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
###############################################################################
# Model Inputs
###############################################################################
saVars = ([i for i in VARS_RANGES if (len(i[1])>1)])
(saNames, saBounds) = list(zip(*saVars))
saNum = len(saVars)
# SA Problem Definition -------------------------------------------------------
problem = {
    'num_vars': saNum,  'names': saNames, 
    'bounds': saBounds, 'dists': ['unif']*saNum
}
###############################################################################
# Sampling
###############################################################################
param_values = saltelli.sample(problem, SAMPLES_NUM)
df = pd.DataFrame(param_values, columns=saNames)
###############################################################################
# Ammending Experiments DF
###############################################################################
rows = df.shape[0]
cstVars = ([i for i in VARS_RANGES if (len(i[1])<=1)])
for (var, cstVal) in cstVars:
    df[var]=cstVal*rows
df = df[[i[0] for i in VARS_RANGES]]
###############################################################################
# Explore
###############################################################################
headerInd = list(df.columns)
uqVal = {i: list(df[i].unique()) for i in headerInd}
df.shape
###############################################################################
# Export
###############################################################################
df.to_csv(path.join(PT_MTR, 'SA_experiment.csv'), index=False)
pkl.dump(problem, path.join(PT_MTR, 'SA_experiment.pkl'))
with open(path.join(PT_MTR, 'SA_experiment.npy'), 'wb') as f:
    np.save(f, param_values)
