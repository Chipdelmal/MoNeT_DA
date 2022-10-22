#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
import numpy as np
from glob import glob
import tGD_aux as aux
from datetime import datetime
import compress_pickle as pkl
from more_itertools import locate
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet

(USR, DRV, AOI, QNT) = ('srv', 'linkedDrive', 'HLT', '50')
probe = "E_499023_499023_007346_039812_941064_739794_01_0192"

exp = '100'
###############################################################################
# Setup ids and paths
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
uids = aux.getExperimentsIDSets(PT_PRE, skip=-1)
(fcs, fcb, fga, fgb, cut, hdr, ren, res, aoi, grp) = uids[1:]
tS = datetime.now()
monet.printExperimentHead(PT_PRE, PT_OUT, tS, 'tGD PstFraction '+AOI)
###############################################################################
# Get data
###############################################################################
aType = ('HLT', 'WLD', 'TRS', 'CST')
fNames = [glob(path.join(PT_OUT, probe+'-{}*'.format(i)))[0] for i in aType]
dta = np.load(fNames[0])
###############################################################################
# Analyze
###############################################################################
avgSig = np.mean(dta, axis=0)