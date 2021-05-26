

import numpy as np
import pandas as pd
from glob import glob
import MoNeT_MGDrivE as monet


# #############################################################################
# Constants
# #############################################################################
OVW = False
(JOB_DSK, JOB_SRV) = (8, 20)
(POP_SIZE, XRAN, FZ, STABLE_T, MLR) = (
    25000*1.25, # 2e6*1.5/2, 
    (0, 5*int(365)), 
    True, 0, False
)
(XP_ID, DRV, XP_PTRN, NO_REL_PAT) = ('QLD', 'IIT', 'E_{}.{}', '00')

# #############################################################################
# Experiments
# #############################################################################
def getExps(LND):
    # if LND=='01':
    return ('s1', 's2', 's3')


# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, EXP, LND):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/QLD/Experiments/{}/'.format(EXP)
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/QLD/Experiments/{}/'.format(EXP)
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)

def selectGeoPath(USR):
    if USR == 'dsk':
        PTH_PTS = '/home/chipdelmal/Documents/WorkSims/QLD/GEO'
    else:
        PTH_PTS = '/RAID5/marshallShare/QLD/GEO'
    return PTH_PTS