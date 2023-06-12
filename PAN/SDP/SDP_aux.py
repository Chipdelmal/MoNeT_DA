
import re
from glob import glob
import MoNeT_MGDrivE as monet

# #############################################################################
# Constants
# #############################################################################
(XP_ID, XP_PTRN, EXPS) = (
    'SDP', 'E_{}_{}-{}_{}_{}.{}',
    ('001', '003')
)
(POP_SIZE, XRAN, FZ, STABLE_T) = (25e3, (0, 365*3), True, 0)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
(DATA_NAMES, DATA_PRE, DATA_PST, DATA_HEAD, MLR) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT', 'DER'),
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD'),
    ( 
        ('i_ren', 1), ('i_res', 2), ('i_grp', 4)
    ),
    False
)
(THI, THO, THW, TAP) = (
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [int((i+1)*365-1) for i in range(5)]
    )
(JOB_DSK, JOB_SRV) = (4, 20)

# #############################################################################
# Names and patterns
# #############################################################################
def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def patternForReleases(ren, AOI, ftype, ext='bz'):
    strPat = XP_PTRN.format(ren, '*', AOI, '*', ftype, ext)
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
        PATH_ROOT = '/RAID5/marshallShare/SplitDrive_Suppression/20230525/{}/{}/'.format(
            DRV, EXP
        )
    elif USR == 'sami':
        PATH_ROOT = '/Users/sanchez.hmsc/Documents/WorkSims/SDP/20230525/{}/{}/'.format(
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
