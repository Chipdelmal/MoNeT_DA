
import re
import random
import matplotlib
import numpy as np
import pandas as pd
from glob import glob
import MoNeT_MGDrivE as monet


# #############################################################################
# Constants
# #############################################################################
OVW = False
(JOB_DSK, JOB_SRV) = (8, 40)
(POP_SIZE, XRAN, FZ, STABLE_T, MLR) = (
    1000000*1.25, # 2e6*1.5/2, 
    (0, 5*int(365)), 
    True, 0, False
)
(XP_ID, DRV, XP_PTRN, NO_REL_PAT) = (
    'STP', 'LDR',
    'E_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}-{}_{}_{}.{}', '00'
)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
(DATA_NAMES, DATA_PRE, DATA_PST) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT', 'DER'),
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD')
)
# Data Analysis ---------------------------------------------------------------
(DATA_HEAD, DATA_SCA) = (
    (
        ('i_sex', 1), ('i_ren', 2), ('i_res', 3), ('i_rsg', 4),
        ('i_gsv', 5), ('i_fcf', 6), ('i_mfm', 7), ('i_mft', 8),
        ('i_hrm', 9), ('i_hrt', 10), ('i_grp', 12)
    ),
    {
        'i_sex': 1  , 'i_ren': 1e0, 'i_res': 1e3, 'i_rsg': 1e10,
        'i_gsv': 1e10,'i_fcf': 1e3, 'i_mfm': 1e3, 'i_mft': 1e3,
        'i_hrm': 1e3, 'i_hrt': 1e3, 'i_grp': 1,   'i_mig': 1e5
    }
)
(THI, THO, THW, TAP) = (
    [.10, .25, .50],
    [.10, .25, .50],
    [.10, .25, .50],
    [int(i) for i in range(0, XRAN[1], int(XRAN[1]/5))]
)
DICE_PARS = (
    ('CPT', 0.01, '#4361ee43'), ('WOP', 2.50, '#ff006e12'), 
    ('TTI', 2.50, '#be0aff13'), ('TTO', 2.50, '#a1ef7a43'), 
    ('POE', 0.01, '#23194212')
)
# ML --------------------------------------------------------------------------
(THS, VT_TRAIN) = ('0.1',  0.3)
(TREES, DEPTH, KFOLD) = (100, 25, 20)
DATA_TYPE = {
    'i_sex': np.int8,
    'i_sxm': np.bool_,  'i_sxg': np.bool_,  'i_sxn': np.bool_,
    'i_ren': np.intc,   'i_res': np.double, 
    'i_rsg': np.double, 'i_gsv': np.double, 'i_fcf': np.double,
    'i_mfm': np.double, 'i_mft': np.double,
    'i_hrm': np.double, 'i_hrt': np.double,
    'i_grp': np.intc,   'i_mig': np.double
}
SEX_CATS = ('i_sxm', 'i_sxg', 'i_sxn')
(ML_CPT_CATS, ML_POE_CATS, ML_POF_CATS) = ( 
    [-.1, .2, .8, 1.1],
    [-.1, .5, 1.1],
    [-.1, .5, 1.1]
)
(ML_WOP_CATS, ML_TTI_CATS, ML_TTO_CATS) = (
    [-10, 365*3, 365*6, 365*11],
    [-10, 60, 90, 120, 150, 365, 365*11],
    [-10, 365*3, 365*6, 365*11]
)
# #############################################################################
# Experiments
# #############################################################################
def getExps(LND):
    if LND=='PAN':
        return ('000000', )
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



