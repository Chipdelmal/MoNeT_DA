#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
from datetime import datetime

from matplotlib.pyplot import vlines
import QLD_aux as aux
import QLD_gene as drv
import QLD_land as lnd
import QLD_functions as fun
# import STP_auxDebug as dbg
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import compress_pickle as pkl


if monet.isNotebook():
    (USR, AOI, LND, EXP) = ('dsk', 'HLT', '02', 's1')
    JOB = aux.JOB_DSK
else:
    (USR, AOI, LND, EXP) = (
        sys.argv[1], sys.argv[2], 
        sys.argv[3],  sys.argv[4]
    )
    JOB = aux.JOB_SRV
EXPS = aux.getExps(LND)
exp = EXP
###########################################################################
# Setting up paths
###########################################################################
(drive, land) = (
    drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(USR, LND)
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, exp, LND
)
PT_IMG = path.join(PT_IMG, 'preTraces')
monet.makeFolder(PT_IMG)
###########################################################################
# Setting up paths
###########################################################################
pthB = "/home/chipdelmal/Documents/WorkSims/s4/POSTPROCESS'E_000-HLT_00.png"
pthA = "/home/chipdelmal/Documents/WorkSims/s1/POSTPROCESS/E_000-HLT_00.png"