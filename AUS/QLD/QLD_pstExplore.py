#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
from datetime import datetime
from matplotlib.pyplot import vlines
import QLD_aux as aux
import QLD_gene as drv
import QLD_land as lnd
import numpy as np
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import compress_pickle as pkl


base = '/home/chipdelmal/Documents/WorkSims/QLD/Experiments/'
year = 3.5
start = int(year*365) # 1175
print('*'*50)
print("  Average signal extrema after {}y".format(year))
print('*'*50)
###########################################################################
# Analyzing seasonality
###########################################################################
pths = (
    "s4/PREPROCESS/E_000-HLT_00_sum.bz",
    "s4/PREPROCESS/E_000-HLT_01_sum.bz"
)
basePopMean = [pkl.load(path.join(base, i))['population'] for i in pths]
totalPop = [i[:,2] for i in basePopMean]
(mx, mn) = ([np.max(i) for i in totalPop], [np.min(i) for i in totalPop])
print('+ Max untreated: {:.0f}, {:.0f}'.format(*mx))
print('+ Min untreated: {:.0f}, {:.0f}'.format(*mn))
print('-'*50)
###########################################################################
# IIT Suppression
###########################################################################
pths = (
    "s1/PREPROCESS/E_007-HLT_00_sum.bz",
    "s1/PREPROCESS/E_007-HLT_01_sum.bz",
)
basePopMean = [pkl.load(path.join(base, i))['population'] for i in pths]
totalPop = [i[:,2][start:] for i in basePopMean]
(mx, mn) = ([np.max(i) for i in totalPop], [np.min(i) for i in totalPop])
print('+ Max IIT: {:.0f}, {:.0f}'.format(*mx))
print('+ Min IIT: {:.0f}, {:.0f}'.format(*mn))
print('-'*50)
###########################################################################
# SRE Suppression
###########################################################################
pths = (
    "s3/PREPROCESS/E_007-HLT_00_sum.bz",
    "s3/PREPROCESS/E_007-HLT_01_sum.bz",
)
basePopMean = [pkl.load(path.join(base, i))['population'] for i in pths]
totalPop = [i[:,2][start:] for i in basePopMean]
(mx, mn) = ([np.max(i) for i in totalPop], [np.min(i) for i in totalPop])
print('+ Max SRE: {:.0f}, {:.0f}'.format(*mx))
print('+ Min SRE: {:.0f}, {:.0f}'.format(*mn))
print('-'*50)
###########################################################################
# IIT+SRE Suppression
###########################################################################
pths = (
    "s2/PREPROCESS/E_007-HLT_00_sum.bz",
    "s2/PREPROCESS/E_007-HLT_01_sum.bz",
)
basePopMean = [pkl.load(path.join(base, i))['population'] for i in pths]
totalPop = [i[:,2][start:] for i in basePopMean]
(mx, mn) = ([np.max(i) for i in totalPop], [np.min(i) for i in totalPop])
print('+ Max IIT+SRE: {:.0f}, {:.0f}'.format(*mx))
print('+ Min IIT+SRE: {:.0f}, {:.0f}'.format(*mn))
print('-'*50)