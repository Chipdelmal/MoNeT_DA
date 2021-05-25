

import numpy as np
import pandas as pd
from glob import glob
import MoNeT_MGDrivE as monet

# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, EXP, LND):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/STP_Grid/{}/{}/'.format(LND, EXP)
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/STP_Grid/{}/{}/'.format(
            LND, EXP
        )
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