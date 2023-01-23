#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import itertools
from os import path
from matplotlib.pyplot import axis
import numpy as np
from glob import glob
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
from more_itertools import locate
import GOP_aux as aux
import GOP_gene as drv


if monet.isNotebook():
    (USR, LND, DRV, AOI, SPE) = ('srv', 'Brikama', 'HUM', 'CSS', 'None')
else:
    (USR, LND, DRV, AOI, SPE) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
(NH, NM) = aux.getPops(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=NM, humSize=NH),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, LND, DRV, SPE
)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_DTA, PT_DTA, tS, 
    '{} PreprocessEpi [{}:{}:{}]'.format(aux.XP_ID, fldr, LND, AOI)
)
# Select sexes and ids --------------------------------------------------------
sexID = {"male": "", "female": "incidence_"}