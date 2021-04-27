

import sys
from os import path
from re import match
from glob import glob
from datetime import datetime
import numpy as np
import pandas as pd
import pingouin as pg
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
from SALib.analyze import sobol
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd

# https://towardsdatascience.com/explaining-feature-importance-by-example-of-a-random-forest-d9166011959e
# https://github.com/parrt/random-forest-importances
# https://explained.ai/rf-importance/index.html
# https://github.com/parrt/random-forest-importances/blob/master/src/rfpimp.py

if monet.isNotebook():
    (USR, LND, AOI, QNT, MTR) = ('dsk', 'PAN', 'HLT', '90', 'CPT')
    JOB = aux.JOB_DSK
else:
    (USR, LND, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
    JOB = aux.JOB_SRV
EXPS = aux.getExps(LND)
###############################################################################
# Paths
###############################################################################
(drive, land) = (
    drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND)
)
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
###############################################################################
# Read CSV
###############################################################################
DATA = pd.read_csv(
    path.join(PT_OUT, 'SCA_{}_{}_{}_qnt.csv'.format(AOI, MTR, QNT))
)
###############################################################################
# Filter Output with Constraints
###############################################################################
fltr = [
    DATA['i_ren'] > 0, DATA['i_ren'] <= 8, 
    DATA['CPT'] > 0.5
]
boolFilter = [all(i) for i in zip(*fltr)]
DATA[boolFilter]
