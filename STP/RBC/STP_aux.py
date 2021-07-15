
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
OVW = True
(JOB_DSK, JOB_SRV) = (8, 60)
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
(DATA_HEAD, DATA_SCA, DATA_PAD) = (
    (
        ('i_sex', 1),   ('i_ren', 2),   ('i_res', 3), 
        ('i_rsg', 4),   ('i_gsv', 5), 
        ('i_fch', 6),   ('i_fcb', 7),   ('i_fcr', 8),
        ('i_hrm', 9),   ('i_hrf', 10), 
        ('i_grp', 12)
    ),
    {
        'i_sex': 1e0,   'i_ren': 1e0,   'i_res': 1e3, 
        'i_rsg': 1e10,  'i_gsv': 1e10,  
        'i_fch': 1e5,   'i_fcb': 1e5,   'i_fcr': 1e5,
        'i_hrm': 1e5,   'i_hrf': 1e5, 
        'i_grp': 1e0,   'i_mig': 1e5
    },
    {
        'i_sex': 2,     'i_ren': 2,     'i_res': 5,   
        'i_rsg': 12,    'i_gsv': 12,  
        'i_fch': 7,     'i_fcb': 7,     'i_fcr': 7,
        'i_hrm': 7,     'i_hrf': 7,   
        'i_grp': 2,     'i_mig': 7
    }
)
(THI, THO, THW, TAP) = (
    [.10, .25, .50],
    [.10, .25, .50],
    [.10, .25, .50],
    [int(i) for i in range(0, XRAN[1], int(XRAN[1]/5))]
)
DICE_PARS = (
    ('CPT', 0.005, '#4361ee43', None),  ('WOP', 0.050, '#ff006e22', None), 
    ('TTO', 0.050, '#00B3E643', None),  ('TTI', 0.075, '#23194233', (0, 150)),
    ('MNF', 0.000, '#be0aff33', None),  ('POE', 0.001, '#00874b33', None)
)
# ML --------------------------------------------------------------------------
(THS, VT_TRAIN) = ('0.1',  0.3)
(TREES, DEPTH, KFOLD) = (100, 15, 20)
DATA_TYPE = {
    'i_sex': np.int8,
    'i_sxm': np.bool_,  'i_sxg': np.bool_,  'i_sxn': np.bool_,
    'i_ren': np.intc,   'i_res': np.double, 
    'i_rsg': np.double, 'i_gsv': np.double, 
    'i_fch': np.double, 'i_fcb': np.double, 'i_fcr': np.double,
    'i_hrm': np.double, 'i_hrf': np.double,
    'i_grp': np.intc,   'i_mig': np.double
}
SEX_CATS = ('i_sxm', 'i_sxg')# , 'i_sxn')
(ML_CPT_CATS, ML_POE_CATS, ML_POF_CATS, ML_MNX_CATS) = ( 
    [-.1, .25, .75, 1.1],
    [-.1, .5, 1.1],
    [-.1, .25, .75, 1.1],
    [-.1, .2, 1.1]
)
(ML_WOP_CATS, ML_TTI_CATS, ML_TTO_CATS) = (
    [-10, 365*1, 365*2, 365*4, 365*6],
    [-10, 60, 365*6],
    [-10, 365*1, 365*2, 365*4,  365*6]
)

# #############################################################################
# Dependent Variables for Heatmaps
# #############################################################################
def selectDepVars(MOI, AOI):
    # Select ranges and dependent variable-------------------------------------
    if (MOI == 'WOP') or (MOI == 'TTI') or (MOI == 'TTO'):
        scalers = [1, 1, XRAN]
        (HD_DEP, IND_RAN) = ('0.1', 7)
    elif (MOI == 'RAP'):
        scalers = [1, 100, 1]
        (HD_DEP, IND_RAN) = ('486', 7)
    elif (MOI == 'MNX'):
        scalers = [1, 100, 1]
        (HD_DEP, IND_RAN) = ('min', 7)
    elif (MOI == 'POE'):
        scalers = [1, 100, 1]
        (HD_DEP, IND_RAN) = ('POE', 1) 
    elif (MOI == 'CPT'):
        scalers = [1, 100, 1]
        (HD_DEP, IND_RAN) = ('CPT', 1) 
    elif (MOI == 'DER'):
        scalers = [1, 100, 5]
        (HD_DEP, IND_RAN) = ('DER', 5) 
    # Color Mapping -----------------------------------------------------------
    if MOI == 'WOP':
        cmap = monet.cmapC
    elif MOI == 'CPT':
        cmap = monet.cmapM
    elif MOI == 'POE':
        cmap = monet.cmapW
    else:
        cmap = monet.cmapW
    return (scalers, HD_DEP, IND_RAN, cmap)

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
def selectPath(USR, EXP, LND, DRV=None):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/STP_Grid/{}/{}/{}/'.format(
            DRV, LND, EXP
        )
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/STP_Grid/{}/{}/{}/'.format(
            DRV, LND, EXP
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



