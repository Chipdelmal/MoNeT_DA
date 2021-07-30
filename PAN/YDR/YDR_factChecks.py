#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
import numpy as np
from glob import glob
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet

if monet.isNotebook():
    (USR, SET, DRV, AOI) = ('lab', 'homing', 'XSD', 'TRS')
else:
    (USR, SET, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
###############################################################################
XP_NPAT = aux.XP_HOM
if SET == 'homing':
    XP_NPAT = aux.XP_SHR
###############################################################################
EXPS = aux.EXPS
exp = EXPS[0]
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=11000),
    lnd.landSelector('SPA')
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, SET, fldr, exp
)
tS = datetime.now()
monet.printExperimentHead(
    PT_DTA, PT_OUT, tS, 
    aux.XP_ID+' PstFraction [{}:{}:{}]'.format(DRV, exp, AOI)
)
###############################################################################
# Mean Max introgression
###############################################################################
fReplace = 'E_048_078_076_079_007_011_011_100_0166666_12-HLT_00_rto.npy'
rats = np.load(path.join(PT_OUT, fReplace))
print("Mean(Max) = {:.3f}". format(1-np.mean([min(i) for i in rats])))