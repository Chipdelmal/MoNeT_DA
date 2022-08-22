
from os import path
import pandas as pd
from SALib.sample import saltelli
import tGD_aux as aux


SAMPLES_NUM = 1024
VARS = ['fcs', 'fcb', 'fga', 'fgb', 'cut', 'hdr', 'res']
(USR, DRV) = ('srv2', 'linkedDrive')
exp = '100'
###############################################################################
# Setup Paths
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
###############################################################################
# Model Inputs
###############################################################################
problem = {
    'num_vars': len(VARS),
    'names': VARS, 
    'bounds': [
        [0, 1], [0, 1],
        [0, 1], [0, 1],
        [0, 1], [0, 1],
        [0, 1]
    ],
    'dists': ['unif']*len(VARS)
}
###############################################################################
# Sampling
###############################################################################
param_values = saltelli.sample(problem, SAMPLES_NUM)
###############################################################################
# Assemble and Export
###############################################################################
df = pd.DataFrame(param_values, columns=VARS)
df.to_csv(path.join(PT_DTA, 'SA_pre.csv'))