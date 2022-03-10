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
import TPT_aux as aux
import TPT_gene as drv


if monet.isNotebook():
    (USR, AOI, DRV) = ('dsk', 'INC', 'LDR')
else:
    (USR, AOI, DRV) = (sys.argv[1], sys.argv[2], sys.argv[3])
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
EXPS = aux.getExps()
exp = EXPS[0]
for exp in EXPS:
    ###########################################################################
    # Setting up paths
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE, humSize=aux.HUM_SIZE),
        aux.landSelector(USR=USR)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, DRV
    )
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_DTA, PT_PRE, tS, 
        '{} PreIncidenceFix [{}:{}:{}]'.format(aux.XP_ID, fldr, exp, AOI)
    )
    # Select sexes and ids ----------------------------------------------------
    sexID = {"male": "", "female": "incidence_"}
    ###########################################################################
    # Load folders
    ###########################################################################
    (expDirsMean, expDirsTrac) = monet.getExpPaths(
        PT_DTA, mean='ANALYZED/', reps='TRACE/'
    )
    ix = 0
    for ix in range(len(expDirsMean)):
        #######################################################################
        # Take averages
        #######################################################################
        fldr = expDirsTrac[ix]
        fldrs = [name for name in os.listdir(fldr) if os.path.isdir(os.path.join(fldr, name))]
        repsFldrs = [fldr+'/'+i+'/' for i in fldrs]
        repsFiles = [glob(i+'/incidence*') for i in repsFldrs]
        repsFiles = [i for i in list(itertools.chain(*repsFiles)) if len(i.split('/')[-1]) >= 18] # DELETE LATER
        repsData = np.asarray([
            np.genfromtxt(rep, delimiter=',', skip_header=1, usecols=[1, 2, 3])
            for rep in repsFiles
        ])
        meanData = np.mean(repsData, axis=0)
        #######################################################################
        # Export csv file
        #######################################################################
        fldr = expDirsMean[ix]
        np.savetxt(
            path.join(fldr, "incidence_Mean_0001.csv"), 
            meanData, delimiter=",", fmt='%f', header="Time, inc_1, NH"
        )

