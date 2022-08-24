
from os import sys
from os import path
import numpy as np
import pandas as pd
import compress_pickle as pkl
from SALib.sample import saltelli
import MoNeT_MGDrivE as monet
import FMS_aux as aux
import FMS_gene as drv


if monet.isNotebook():
    (USR, DRV) = ('srv', 'PGS')
else:
    (USR, DRV) = sys.argv[1:]
###############################################################################
# Setting Paths Up and Reading SA Constants
###############################################################################
(SAMPLES_NUM, VARS_RANGES) = (aux.SA_SAMPLES, aux.SA_RANGES)
(drive, land) = (
    drv.driveSelector(DRV, 'HLT', popSize=aux.POP_SIZE), aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, fldr)
###############################################################################
# Read
###############################################################################
problem = pkl.load(path.join(PT_MTR, 'SA_experiment.pkl'))
sampler = np.load(path.join(PT_MTR, 'SA_experiment.npy'))
df = pd.read_csv (path.join(PT_MTR, 'SA_experiment.csv'))