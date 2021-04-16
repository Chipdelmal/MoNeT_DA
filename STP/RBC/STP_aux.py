
import re
import matplotlib
import pandas as pd
from glob import glob
import MoNeT_MGDrivE as monet

# #############################################################################
# Constants
# pop=1.25e6
# #############################################################################
(POP_SIZE, XRAN, FZ, STABLE_T, MLR) = (2e6*1.5/2, (0, int(365*5)), True, 0, True)
(XP_ID, DRV, OVW, XP_PTRN, NO_REL_PAT) = (
    'STP', 'LDR', False,
    'E_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}-{}_{}_{}.{}', '00'
)
(SUM, AGG, SPA, REP, SRP, OVW) = (True, False, False, False, True, True)
(DATA_NAMES, DATA_PRE, DATA_PST, DATA_HEAD) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT', 'DER'),
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD'),
    (
        ('i_sex', 1), ('i_ren', 2), ('i_res', 3), ('i_rsg', 4),
        ('i_gsv', 5), ('i_fcf', 6), ('i_mfm', 7), ('i_mft', 8),
        ('i_hrm', 9), ('i_hrt', 10), ('i_grp', 12)
    )
)
(THI, THO, THW, TAP) = (
    [.05, .10, .25, .50, .75, .90, .95],
    [.05, .10, .25, .50, .75, .90, .95],
    [.05, .10, .25, .50, .75, .90, .95],
    [int(i) for i in range(0, XRAN[1], int(XRAN[1]/10))]
)
(JOB_DSK, JOB_SRV) = (4, 8)


# #############################################################################
# Experiments
# #############################################################################
def getExps(LND):
    if LND=='PAN':
        return ('000000', '000001')
    else:
        return ('265_S', '265_P')

# #############################################################################
# Names and patterns
# #############################################################################
def patternForReleases(ren, AOI, ftype, ext='bz'):
    strPat = XP_PTRN.format(
        '*', ren, '*', '*', '*', 
        '*', '*', '*', '*', '*', 
        AOI, '*', ftype, ext
    )
    return strPat


def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


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


