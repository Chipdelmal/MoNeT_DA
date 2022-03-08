#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
from glob import glob
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
from more_itertools import locate
import pandas as pd
import TPT_aux as aux
import TPT_gene as drv


if monet.isNotebook():
    (USR, AOI, DRV, QNT) = ('dsk', 'HUM', 'LDR', '50')
else:
    (USR, AOI, DRV, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###############################################################################
# Get Experiments and Offset
###############################################################################
(EXPS, REL_START) = (aux.getExps(), aux.landSelector(USR=USR))
###############################################################################
# Processing loop
###############################################################################
exp = EXPS[-1]
fname = "E_05_00500_000790000000_000100000000_0000000_0017550_0000000_0100000_0095600-HUM_00_rto.npy"

(header, xpidIx) = list(zip(*aux.DATA_HEAD))
###########################################################################
# Load landscape and drive
###########################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE, humSize=aux.HUM_SIZE),
    aux.landSelector(USR=USR)
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, exp, DRV
)

min(np.load(PT_OUT+fname)[0])