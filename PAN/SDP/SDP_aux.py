
import re
import matplotlib
import pandas as pd
from glob import glob
import MoNeT_MGDrivE as monet

# #############################################################################
# Constants
# #############################################################################
(XP_ID, XP_PTRN, EXPS) = (
    'SDP', 'E_{}_{}_{}_{}_{}-{}_{}_{}.{}',
    ('000', '001') #, '010')
)
(POP_SIZE, XRAN, FZ, STABLE_T) = (25e3, (0, 365*2.5), True, 0)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
(DATA_NAMES, DATA_PRE, DATA_PST, DATA_HEAD, MLR) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT', 'DER'),
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD'),
    (
        ('i_par', 1), ('i_csa', 2), ('i_csb', 3), 
        ('i_ren', 4), ('i_res', 5), ('i_grp', 7)
    ),
    False
)
(THI, THO, THW, TAP) = (
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [int((i+1)*365-1) for i in range(5)]
    )
(JOB_DSK, JOB_SRV) = (4, 40)

# #############################################################################
# Names and patterns
# #############################################################################
def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def patternForReleases(ren, AOI, ftype, ext='bz'):
    strPat = XP_PTRN.format('*', '*', '*', ren, '*', AOI, '*', ftype, ext)
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
    elif USR == 'srv2':
        PATH_ROOT = '/RAID5/marshallShare/SplitDrive_Suppression/theoretical/{}/{}/'.format(
            DRV, EXP
        )
    elif USR == 'srvA':
        PATH_ROOT = '/RAID5/marshallShare/SplitDrive_Suppression/realized1/{}/{}/'.format(
            DRV, EXP
        )
    elif USR == 'srvB':
        PATH_ROOT = '/RAID5/marshallShare/SplitDrive_Suppression/realized2/{}/{}/'.format(
            DRV, EXP
        )
    elif USR == 'srvC':
        PATH_ROOT = '/RAID5/marshallShare/SplitDrive_Suppression/realized3/{}/{}/'.format(
            DRV, EXP
        )
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/SDP/{}/{}/'.format(
            DRV, EXP
        )
    elif USR == 'lab':
         PATH_ROOT = '/Volumes/marshallShare/SplitDrive_Suppression/theoretical/{}/{}/'.format(
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
