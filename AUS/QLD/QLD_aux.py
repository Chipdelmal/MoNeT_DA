
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
    30000*2*2, # 2e6*1.5/2, 
    (0, 5*int(365)), 
    True, 0, False
)
(XP_ID, DRV, XP_PTRN, NO_REL_PAT) = ('QLD', 'IIT', 'E_{}-{}_{}_{}.{}', '000')
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)

# #############################################################################
# Experiments
# #############################################################################
def getExps(LND):
    return ('s1', 's2', 's3', 's4')

REL = ('1e-06', )# '1e-07', '1e-08', '1e-09', '1e-10')

# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, EXP, LND, REL):
    if USR == 'srvA':
        PATH_ROOT = '/RAID5/marshallShare/QLD/20220822_A/1e-06/{}/'.format(EXP)
    elif USR == 'srvB':
        PATH_ROOT = '/RAID5/marshallShare/QLD/20220822_B/1e-06/{}/'.format(EXP)
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/QLD/Experiments/{}/'.format(EXP)
    elif USR == 'dsk2':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/QLD/ExperimentsB/{}/'.format(EXP)
    elif USR == 'dsk3':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/QLD/ExperimentsC/{}/'.format(EXP)
    elif USR == 'lab31':
        PATH_ROOT = '/Users/sanchez.hmsc/Desktop/QLD/year3/Experiments/{}/{}/'.format(REL, EXP)
    elif USR == 'lab33':
        PATH_ROOT = '/Users/sanchez.hmsc/Desktop/QLD/year3/ExperimentsC/{}/{}/'.format(REL, EXP)
    elif USR == 'lab41':
        PATH_ROOT = '/Users/sanchez.hmsc/Desktop/QLD/year4/Experiments/{}/{}/'.format(REL, EXP)
    elif USR == 'lab43':
        PATH_ROOT = '/Users/sanchez.hmsc/Desktop/QLD/year4/ExperimentsC/{}/{}/'.format(REL, EXP)
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
    if (USR=='lab31') or (USR=='lab33') or (USR=='lab41') or (USR=='lab43'):
        PTH_PTS = '/Users/sanchez.hmsc/Desktop/QLD/GEO'
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