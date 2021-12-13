#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import pandas as pd
from os import path
from sys import argv
from copy import deepcopy
import matplotlib.pyplot as plt
from compress_pickle import dump, load
import MGSurvE as srv
import warnings
warnings.filterwarnings('ignore', 'The iteration is not making good progress')


if srv.isNotebook():
    (OUT_PTH, LND_TYPE, ID) = (
        '/home/chipdelmal/Documents/WorkSims/MGSurvE_Benchmarks/Sex/', 
        'UNIF', 'SX10'
    )
else:
    (OUT_PTH, LND_TYPE, ID) = (
        argv[1], argv[2], argv[3].zfill(3)
    )
TRPS_NUM=3
ID="{}-{:03d}".format(ID, TRPS_NUM)
###############################################################################
# Defining Landscape and Traps
###############################################################################
if LND_TYPE == 'UNIF':
    ptsNum = 400
    bbox = ((-225, 225), (-175, 175))
    xy = srv.ptsRandUniform(ptsNum, bbox).T
elif LND_TYPE == 'GRID':
    ptsNum = 20
    bbox = ((-225, 225), (-225, 225))
    xy = srv.ptsRegularGrid(ptsNum, bbox).T
elif LND_TYPE == 'DNUT':
    ptsNum = 300
    radii = (100, 150)
    xy = srv.ptsDonut(ptsNum, radii).T
points = pd.DataFrame({'x': xy[0], 'y': xy[1], 't': [0]*xy.shape[1]})
# Traps info ------------------------------------------------------------------
nullTraps = [0] * TRPS_NUM
traps = pd.DataFrame({
    'x': nullTraps, 'y': nullTraps, 'f': nullTraps,
    't': [0, 0, 0]
})
tKernels = {
    'Male': {
        0: {'kernel': srv.exponentialDecay, 'params': {'A': .5, 'b': .1}}
    },
    'Female': {
        0: {'kernel': srv.exponentialDecay, 'params': {'A': .3, 'b': .06}}
    }
}
trapsRadii = [.1, ]
###############################################################################
# Defining Movement
###############################################################################
movementKernel = {
    'Male': {
        'kernelFunction': srv.zeroInflatedExponentialKernel,
        'kernelParams': {
            'params': [.075, 1.0e-10, math.inf], 'zeroInflation': .5
        }
    },
    'Female': {
        'kernelFunction': srv.zeroInflatedExponentialKernel,
        'kernelParams': {
            'params': [.075, 1.0e-10, math.inf], 'zeroInflation': .6
        }
    }
}
###############################################################################
# Setting Landscape Up
###############################################################################
lndM = srv.Landscape(
    points, traps=traps,
    kernelFunction=movementKernel['Male']['kernelFunction'],
    kernelParams=movementKernel['Male']['kernelParams'],
    trapsKernels=tKernels['Male'], trapsRadii=trapsRadii
)
lndF = srv.Landscape(
    points, traps=traps,
    kernelFunction=movementKernel['Female']['kernelFunction'],
    kernelParams=movementKernel['Female']['kernelParams'],
    trapsKernels=tKernels['Female'], trapsRadii=trapsRadii
)
srv.dumpLandscape(lndM, OUT_PTH, '{}_{}_M_CLN'.format(LND_TYPE, ID))
srv.dumpLandscape(lndF, OUT_PTH, '{}_{}_F_CLN'.format(LND_TYPE, ID))