#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import operator as op
from os import path
import numpy as np
from glob import glob
import tGD_aux as aux
import matplotlib.pyplot as plt
from datetime import datetime
import compress_pickle as pkl
from more_itertools import locate
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet

(USR, DRV, AOI, QNT) = ('srv2', 'splitDrive', 'TRS', '50')
probe = "E_3500_3500_0000_0427_100_090_12_0100"

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
ix = aType.index(AOI)
fNames = [glob(path.join(PT_OUT, probe+'-{}*'.format(i)))[0] for i in aType]
dta = np.load(fNames[ix])
###############################################################################
# Analyze
###############################################################################
avgSig = np.mean(dta, axis=0)
minWild = np.min(avgSig)
boolList = monet.comparePopToThresh(avgSig, [minWild, ], cmprOp=op.le)
minTime = monet.trueIndices(boolList)[0]
print(f'{minWild} ({1-minWild}) @ {minTime}')
plt.plot(avgSig)