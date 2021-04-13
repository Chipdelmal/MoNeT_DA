

import re
import matplotlib
import pandas as pd
# import numpy as np
from glob import glob
from os import path
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


XP_ID = 'YDR'
(XP_HOM, XP_SHR) = (
    'E_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}-{}_{}_{}.{}',
    'E_{}_{}_{}_{}_{}_{}_{}_{}-{}_{}_{}.{}'
)
(POP_SIZE, XRAN, FZ, STABLE_T) = (20e3*1.25, (0, (365*5)), True, 0)
EXPS = ('000', '002', '004', '006', '008')
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
(DATA_NAMES, DATA_PRE, DATA_PST, MLR) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT', 'DER'), 
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD'),
    True
)
(THI, THO, THW, TAP) = (
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [int((i+1)*365-1) for i in range(5)]
    )
FRATE = 30
(JOB_DSK, JOB_SRV) = (8, 30)

# #############################################################################
# Experiment-Specific Path Functions
# #############################################################################
def getXPPattern(SET):
    if SET == 'homing':
        return XP_HOM
    else:
        return XP_SHR


def patternForReleases(SET, ren, AOI, ftype, ext='bz'):
    if SET == 'homing':
        patList = ['*','*','*','*','*','*','*','*','*',ren,AOI,'*',ftype,ext]
        return XP_HOM.format(*patList)
    else:
        patList = ['*','*','*','*','*','*','*',ren,AOI,'*',ftype,ext]
        return XP_SHR.format(*patList)


def getSummaryHeader(SET):
    if SET == 'homing':
        DATA_HEAD = (
            ('i_mcl', 1), ('i_fcl', 2), ('i_mhr', 3), ('i_fhr', 4), 
            ('i_res', 5), ('i_cac', 6), ('i_gac', 7), ('i_bac', 8), 
            ('i_ref', 9), ('i_ren', 10), ('i_grp', 12)
        )
    else:
        DATA_HEAD = (
            ('i_mcl', 1), ('i_fcl', 2), ('i_mrs', 3), ('i_frs', 4), 
            ('i_atc', 5), ('i_rac', 6), ('i_ref', 7), ('i_ren', 8), 
            ('i_grp', 10)    
        )
    return DATA_HEAD


# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, SET, DRV, EXP):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/yLinked/{}/{}/{}/'.format(SET, DRV, EXP)
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/YDR/{}/{}/{}/'.format(SET, DRV, EXP)
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)


def selectDepVars(MOI, THS, AOI):
    # Select ranges and dependent variable-------------------------------------
    if (MOI == 'WOP'):
        scalers = (1, 1000, round(450))
        (HD_DEP, IND_RAN) = (str(THS), 7)
    elif (MOI == 'TTI'):
        scalers = (1, 1000, round(250))
        (HD_DEP, IND_RAN) = (str(THS), 7)
    elif (MOI == 'TTO'):
        scalers = (1, 1000, round(610))
        (HD_DEP, IND_RAN) = (str(THS), 7)
    elif (MOI == 'RAP'):
        scalers = (1, 1000, 1)
        (HD_DEP, IND_RAN) = ('486', 7)
    elif (MOI == 'MNX'):
        scalers = (1, 1000, 1)
        (HD_DEP, IND_RAN) = ('min', 7)
    # Color Mapping -----------------------------------------------------------
    if AOI == 'HLT':
        cmap = monet.cmapC
    elif AOI == 'TRS':
        cmap = monet.cmapM
    elif AOI == 'WLD':
        cmap = monet.cmapW
    return (scalers, HD_DEP, IND_RAN, cmap)


# #############################################################################
# Paths and Names
# #############################################################################
def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def getExperimentsIDSets(PATH_EXP, skip=-1, ext='.bz'):
    filesList = glob(PATH_EXP+'/E*')
    fileNames = [i.split('/')[-1].split('.')[-2] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids


# #############################################################################
# Style
# #############################################################################
def getStyle(colors, aspectR, xRange, yRange):
    style = {
            "width": .1, "alpha": .1, "dpi": 500,
            "legend": True, "aspect": .5,
            "xRange": xRange, "yRange": yRange,
            "colors": colors
        }
    style['aspect'] = monet.scaleAspect(aspectR, style)
    return style


