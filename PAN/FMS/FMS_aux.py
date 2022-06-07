#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from glob import glob
import MoNeT_MGDrivE as monet

XP_ID = 'FMS'
###############################################################################
# System Constants
###############################################################################
(OVW, JOB_DSK, JOB_SRV) = (True, 4, 20)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
###############################################################################
# Releases and Populations
###############################################################################
(REL_START, RELEASES) = (50, [365+(7*i) for i in range(10)])
(POP_SIZE, HUM_SIZE, INC_SIZE, XRAN, FZ) = (
    5e3, 1e3, 1000*1.25,
    (0, 5*int(365)), 
    False
)
(STABLE_T, MLR, SAMP_RATE) = (0, False, 1)
###############################################################################
# Files and DA constants
###############################################################################
(XP_PTRN, NO_REL_PAT) = ('E_{}_{}_{}_{}_{}_{}_{}_{}_{}-{}_{}_{}.{}', '00')
REF_FILE = 'E_00_00000_00000000000_000000000000_0000000_0000000_0000000_0000000_0000000'
(DATA_NAMES, DATA_PRE, DATA_PST) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT'),
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD')
)
# Data Analysis ---------------------------------------------------------------
(DATA_HEAD, DATA_SCA, DATA_PAD) = (
    (
        ('i_ren', 1),   ('i_rer', 2),
        ('i_rsg', 3),   ('i_gsv', 4), 
        ('i_fch', 5),   ('i_fcb', 6),   ('i_fcr', 7),
        ('i_hrm', 8),   ('i_hrf', 9)
    ),
    {
        'i_ren': 1e0,   'i_rer': 1e3,   
        'i_rsg': 1e9,   'i_gsv': 1e10,  
        'i_fch': 1e5,   'i_fcb': 1e5,   'i_fcr': 1e5,
        'i_hrm': 1e5,   'i_hrf': 1e5
    },
    {
        'i_ren': 2,     'i_rer': 2,     
        'i_rsg': 12,    'i_gsv': 12,  
        'i_fch': 7,     'i_fcb': 7,     'i_fcr': 7,
        'i_hrm': 7,     'i_hrf': 7
    }
)
(THI, THO, THW, TAP) = (
    [.10, .25, .50, .75, .90],
    [.10, .25, .50, .75, .90],
    [.10, .25, .50, .75, .90],
    [0, 365]
)
###############################################################################
# Dependent Variables for Heatmaps
###############################################################################
def selectDepVars(MOI, AOI):
    # Select ranges and dependent variable-------------------------------------
    if (MOI == 'WOP') or (MOI == 'TTO'):
        scalers = [1, 1, XRAN]
        (HD_DEP, IND_RAN) = ('0.1', 7)
    elif (MOI == 'TTI'):
        scalers = [1, 1, XRAN]
        (HD_DEP, IND_RAN) = ('0.1', 7)
    elif (MOI == 'RAP'):
        scalers = [1, 100, 90]
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
    elif (MOI == 'MNF'):
        scalers = [1, 1, 1]
        (HD_DEP, IND_RAN) = ('MNF', 1) 
    # Color Mapping -----------------------------------------------------------
    if MOI == 'WOP':
        cmap = monet.cmapP
    elif MOI == 'CPT':
        cmap = monet.cmapM
    elif MOI == 'POE':
        cmap = monet.cmapC
    else:
        cmap = monet.cmapW
    return (scalers, HD_DEP, IND_RAN, cmap)

###############################################################################
# Experiments
###############################################################################
def getExps():
    return ('A', 'B')

###############################################################################
# Names and patterns
###############################################################################
def patternForReleases(ren, AOI, ftype, ext='bz'):
    strPat = XP_PTRN.format(
        ren, '*', '*', '*', 
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


###############################################################################
# Paths
###############################################################################
def selectPath(USR, DRV=None):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/fem_pgSIT/{}/'.format(DRV)
    elif USR == 'lab':
        PATH_ROOT = '/Volumes/marshallShare/fem_pgSIT/{}/'.format(DRV)
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/fem_pgSIT/{}/'.format(DRV)
    (PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT), 
        '{}'.format(PATH_ROOT)
    )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)


def landSelector(USR='lab'):
    PAN = ([0], )
    return PAN


def replaceExpBase(tracePath, refFile):
    head = '/'.join(tracePath.split('/')[:-1])
    tail = tracePath.split('-')[-1]
    return '{}/{}-{}'.format(head, refFile, tail)


def chunks(l, n):
    (d, r) = divmod(len(l), n)
    for i in range(n):
        si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
        yield l[si:si+(d+1 if i < r else d)]
