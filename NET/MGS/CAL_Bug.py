#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from os import path
from copy import deepcopy
import matplotlib.pyplot as plt
import MGSurvE as srv
import cartopy.crs as ccrs


GENS = 2000
(PTH_O, PTH_I) = ('./out', './in')
###############################################################################
# Load Pointset
###############################################################################
SITES = pd.read_csv(path.join(PTH_I, 'LatLon_Yap.csv'))
SITES['t'] = [0]*SITES.shape[0]
SITES_bbox = (
    (min(SITES['lon']), max(SITES['lon'])),
    (min(SITES['lat']), max(SITES['lat']))
)
SITES_cntr = [i[0]+(i[1]-i[0])/2 for i in SITES_bbox]
###############################################################################
# Movement Kernel
###############################################################################
mKer = {'params':srv.AEDES_EXP_PARAMS, 'zeroInflation': .2}
###############################################################################
# Traps
###############################################################################
traps = pd.DataFrame({
    'lon': [SITES_cntr[0]]*4, 
    'lat': [SITES_cntr[1]]*4, 
    'f': [0, 0, 0, 0],
    't': [0, 0, 0, 1]
})
tKer = {
    0: {'kernel': srv.exponentialDecay, 'params': {'A': 1, 'b': .0075}},
    1: {'kernel': srv.exponentialDecay, 'params': {'A': 1, 'b': .0050}},
}
###############################################################################
# Setting Landscape Up
###############################################################################
lnd = srv.Landscape(
    SITES, # landLimits=SITES_bbox,
    kernelParams=mKer,
    traps=traps, trapsKernels=tKer,
    trapsRadii=[.75, .5, .3],
)
bbox = lnd.getBoundingBox()
trpMsk = srv.genFixedTrapsMask(lnd.trapsFixed)