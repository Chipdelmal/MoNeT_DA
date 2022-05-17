#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from glob import glob
import numpy as np
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import TPT_aux as aux
import TPT_gene as drv

if monet.isNotebook():
    (USR, AOI, DRV, SPE) = ('lab', 'INC', 'LDR', 'gambiae_low')
else:
    (USR, AOI, DRV, SPE) = sys.argv[1:]
GRID_REF = False


EXPS = aux.getExps()
exp = EXPS[0]
###########################################################################
# Setup paths and drive
###########################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE, humSize=aux.HUM_SIZE),
    aux.landSelector(USR=USR)
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, exp, DRV, SPE
)
###########################################################################
# Load Data
###########################################################################
pth = (PT_PRE + aux.REF_FILE + '-ECO_00_sum.bz')
dta = pkl.load(pth)
pop = (dta['population'].T[-1])
(np.quantile(pop, .25), np.mean(pop), np.quantile(pop, .75))