

import sys
from glob import glob
from datetime import datetime
from os import path
from re import match
import numpy as np
import pandas as pd
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd


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
(PT_IMG, PT_OUT) = (PT_ROT+'preTraces/', PT_ROT+'ML')
[monet.makeFolder(i) for i in [PT_IMG, PT_OUT]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
###############################################################################
# Flatten CSVs
###############################################################################
i = PT_SUMS[0]
fName = glob('{}/*{}*{}*.bz'.format(i, AOI, 'WOP'))[0]

###############################################################################
# Load MLR dataset
###############################################################################
i = PT_SUMS[0]
fName = glob('{}/*{}*{}*.bz'.format(i, AOI, 'WOP'))[0]
probe = pkl.load(fName)
keys = list(probe.keys())
[probe[j] for j in keys]


probe[keys[5]]