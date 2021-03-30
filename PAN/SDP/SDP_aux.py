
import re
import matplotlib
import pandas as pd
from glob import glob
import MoNeT_MGDrivE as monet

# #############################################################################
# Constants
# #############################################################################
XP_PTRN = 'E_{}_{}_{}_{}_{}-{}_{}_{}.{}'
EXPS = ('000', '001', '010')
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
(POP_SIZE, XRAN) = (25e3, (0, 365*2.5))
FZ = True

# #############################################################################
# Names and patterns
# #############################################################################
def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def patternForReleases(ren, AOI, ftype):
    strPat = XP_PTRN.format('*', '*', '*', ren, '*', AOI, '*', ftype, 'bz')
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


# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, DRV, EXP):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/SplitDrive_Suppression/{}/{}/'.format(
            DRV, EXP
        )
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/SDP/{}/{}/'.format(
            DRV, EXP
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