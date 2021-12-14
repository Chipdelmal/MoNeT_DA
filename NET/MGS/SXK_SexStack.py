#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pandas as pd
from os import path
from sys import argv
from copy import deepcopy
import matplotlib.pyplot as plt
from compress_pickle import dump, load
import MGSurvE as srv
from PIL import Image


(GENS, VERBOSE) = (500, False)
if srv.isNotebook():
    (OUT_PTH, LND_TYPE, ID, TRPS_NUM) = (
        '/home/chipdelmal/Documents/WorkSims/MGSurvE_Benchmarks/SX_BENCH/', 
        'UNIF', 'SX4', 6
    )
else:
    (OUT_PTH, LND_TYPE, ID, TRPS_NUM) = (argv[1], argv[2], argv[3].zfill(3), int(argv[4]))
ID="{}-{:03d}".format(ID, TRPS_NUM)
scaler = 2
###############################################################################
# Concatenate Images
###############################################################################
imgPaths = (
    path.join(OUT_PTH, '{}_{}-M_TRP.png'.format(LND_TYPE, ID)),
    path.join(OUT_PTH, '{}_{}-F_TRP.png'.format(LND_TYPE, ID)),
    path.join(OUT_PTH, '{}_{}-B_TRP.png'.format(LND_TYPE, ID))
)
(imgM, imgF, imgB) = [cv2.imread(i) for i in imgPaths]
dim = imgM.shape
partA = np.vstack((imgM, imgF))
dimA = partA.shape
imgFull = np.hstack((partA, cv2.resize(imgB, (int(dimA[1]*scaler), int(imgB.shape[0]*2)))))
###############################################################################
# Write to Disk
###############################################################################
OUT_PTH = path.join(OUT_PTH, 'img')
srv.makeFolder(OUT_PTH)
cv2.imwrite(path.join(OUT_PTH, '{}-TRP.png'.format(ID)), imgFull)
