
import re
import numpy as np
import pandas as pd
from glob import glob
import MoNeT_MGDrivE as monet


# #############################################################################
# Constants
# #############################################################################
OVW = True
(JOB_DSK, JOB_SRV) = (8, 20)
(POP_SIZE, XRAN, FZ, STABLE_T, MLR) = (
    50000*2, # 2e6*1.5/2, 
    (0, 5*int(365)), 
    True, 0, False
)
(XP_ID, DRV, XP_PTRN, NO_REL_PAT) = ('QLD', 'IIT', 'E_{}-{}_{}_{}.{}', '000')
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)

# #############################################################################
# Experiments
# #############################################################################
def getExps(LND):
    # if LND=='01':
    return ('s1', )# , 's2', 's3', 's4')


# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, EXP, LND):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/QLD/Experiments/{}/'.format(EXP)
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/QLD/Experiments/{}/'.format(EXP)
    elif USR == 'dsk2':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/QLD/ExperimentsB/{}/'.format(EXP)
    elif USR == 'dsk3':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/QLD/ExperimentsC/{}/'.format(EXP)
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
    elif USR == 'dsk2':
        PTH_PTS = '/home/chipdelmal/Documents/WorkSims/QLD/GEO'
    elif USR == 'dsk3':
        PTH_PTS = '/home/chipdelmal/Documents/WorkSims/QLD/GEO'
    else:
        PTH_PTS = '/RAID5/marshallShare/QLD/GEO'
    return PTH_PTS


def patternForReleases(ren, AOI, ftype, ext='bz'):
    strPat = XP_PTRN.format(
        ren, AOI, '*', ftype, ext
    )
    return strPat


def getExperimentsIDSets(PATH_EXP, skip=-1, ext='.bz'):
    filesList = glob(PATH_EXP+'E*')
    fileNames = [i.split('/')[-1].split('.')[-2] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids