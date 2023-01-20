#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np
from numpy import random
from glob import glob
from more_itertools import locate
from os import path
import compress_pickle as pkl
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
from matplotlib.colors import LinearSegmentedColormap, ColorConverter
import warnings
warnings.filterwarnings("ignore")


XP_ID = 'GOP'
###############################################################################
# System Constants
###############################################################################
(OVW, JOB_DSK, JOB_SRV) = (True, 4, 20)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
###############################################################################
# Releases and Populations
###############################################################################
(REL_START, RELEASES) = (5, [365+(7*i) for i in range(10)])
(POP_SIZE, HUM_SIZE, INC_SIZE, XRAN, FZ) = (
    5e3, 1e3, 1000*1.25,
    (REL_START, 10*int(365)), 
    False
)
(STABLE_T, MLR, SAMP_RATE) = (0, False, 1)
MAX_REPS = 100
###############################################################################
# Sensitivity Analysis
###############################################################################
SA_SAMPLES = 2**17
SA_RANGES = (
    ('ren', (1, 48)), 
    ('rer', (1, 50)), 
    ('rei', (1, 20)),
    ('pct', (.5, 1)), 
    ('pmd', (.5, 1)), 
    ('mfr', (0, .5)), 
    ('mtf', (.5, 1)), 
    ('fvb', (0, .5))
)
SA_MONOTONIC_WOP = {
    'i_ren': 0, 'i_res': 0, 'i_rei': 0,
    'i_pct': 1, 'i_pmd': 1,
    'i_mfr': -1, 'i_mtf': 1, 'i_fvb': -1
}
SA_MONOTONIC_CPT = {
    'i_ren': 0, 'i_res': 0, 'i_rei': 0,
    'i_pct': -1, 'i_pmd': -1,
    'i_mfr': 1, 'i_mtf': -1, 'i_fvb': 1
}
###############################################################################
# Files and DA constants
#   "ren", "rer", "rei", "pct", "pmd", "mfr", "mtf", "fvb"
#   1e0, 1e8, 1e0, 1e10, 1e10, 1e10, 1e10, 1e10
#   4, 14, 4, 12, 12, 12, 12, 12
###############################################################################
(XP_PTRN, NO_REL_PAT) = ('E_{}_{}_{}_{}_{}_{}_{}_{}-{}_{}_{}.{}', '00')
(DATA_NAMES, DATA_PRE, DATA_PST) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT'),
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD')
)
# Data Analysis ---------------------------------------------------------------
(DATA_HEAD, DATA_SCA, DATA_PAD, DATA_TYPE) = (
    (
        ('i_ren', 1), ('i_res', 2), ('i_rei', 3),
        ('i_pct', 4), ('i_pmd', 5), 
        ('i_mfr', 6), ('i_mtf', 7), ('i_fvb', 8),
        ('i_grp', 10)
    ),
    {
        'i_ren': 1e0,  'i_res': 1e8, 'i_rei': 1e0,
        'i_pct': 1e10, 'i_pmd': 1e10, 
        'i_mfr': 1e10, 'i_mtf': 1e10, 'i_fvb': 1e10,
        'i_grp': 1e0
    },
    {
        'i_ren': 4,  'i_res': 14, 'i_rei': 4,
        'i_pct': 12, 'i_pmd': 12, 
        'i_mfr': 12, 'i_mtf': 12, 'i_fvb': 12,
        'i_grp': 2
    },
    {
        'i_ren': np.int8,   'i_res': np.double, 'i_rei': np.int8,
        'i_pct': np.double, 'i_pmd': np.double, 
        'i_mfr': np.double, 'i_mtf': np.double, 'i_fvb': np.double,
        'i_grp': np.int8
    }
)
(THI, THO, THW, TAP) = (
    [.10, .20, .25, .50, .75, .80, .90],
    [.10, .20, .25, .50, .75, .80, .90],
    [.10, .20, .25, .50, .75, .80, .90],
    [0, 365]
)
# REF_FILE = 'E_0000_00000000000000_0000_000000000000_000000000000_000000000000_000000000000_000000000000'
REF_FILE = 'E_'+'_'.join(['0'*i for i in list(DATA_PAD.values())[:-1]])
###############################################################################
# DICE Plots
###############################################################################
pFeats = (
    ('i_ren', 'linear'), ('i_res', 'linear'), ('i_rei', 'linear'),
    ('i_pct', 'linear'), ('i_pmd', 'linear'),
    ('i_mfr', 'linear'), ('i_mtf', 'linear'), ('i_fvb', 'linear'),
)
DICE_PARS = (
    ('CPT', 0.005, '#4361ee43', (0, 1)),
    ('WOP', 0.050, '#be0aff33', (0, 5*365+50)),
    ('TTO', 0.050, '#9ef01a33', (0, 5*365+50)),
    ('TTI', 0.075, '#23194233', (0, 150)),
    ('MNF', 0.000, '#00B3E643', (0, 1)),
    ('POE', 0.001, '#ff006e22', (0, 1))
)
###############################################################################
# Dependent Variables for Heatmaps
###############################################################################
def colorPaletteFromHexList(clist):
    c = ColorConverter().to_rgba
    clrs = [c(i) for i in clist]
    rvb = LinearSegmentedColormap.from_list("", clrs)
    return rvb

def selectDepVars(MOI):
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
        cmap = colorPaletteFromHexList(['#ffffff00', '#3687ff33'])
    elif MOI == 'CPT':
        cmap = colorPaletteFromHexList(['#ffffff00', '#2614ed55'])
    elif MOI == 'POE':
        cmap = colorPaletteFromHexList(['#ffffff00', '#8338EC55'])
    else:
        cmap = colorPaletteFromHexList(['#ffffff00', '#3b479d55'])
    return (scalers, HD_DEP, IND_RAN, cmap)

###############################################################################
# Experiments
###############################################################################
def getExps():
    return ('A', 'B')

###############################################################################
# Names and patterns
###############################################################################
def patternForReleases(ren, AOI, ftype, ext='bz', pad=0):
    renP = str(ren).rjust(pad, '0')
    strPat = XP_PTRN.format(
        renP, '*', '*', '*', '*', '*', '*', '*', 
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
def selectPath(USR, LND, DRV, SPE):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/GambiaOP/{}/'.format(LND)
    elif USR == 'dsk':
        PATH_ROOT = '/RAID5/marshallShare/GambiaOP/{}/'.format(LND)
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


def landSelector():
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

###############################################################################
# Epi
###############################################################################
def findEpiGroupsIndices(genotypes, classID, groupsList):
    fMatches = []
    for grp in groupsList:
        matches = [s for s in genotypes if classID+grp in s]
        fMatches.extend(matches)
    ixMatches = [genotypes.index(m) for m in fMatches]
    return ixMatches

def humanGroupsToGeneDict(statDict, stratum, genotypes):
    hDict = {}
    for k in statDict:
        elms = statDict[k]
        # Get the indices from all the elements in the group
        grp = []
        for e in elms:
            grp.extend(findEpiGroupsIndices(genotypes, e, stratum))
        # Add to the dictionary with group ID
        hDict[k] = grp
    return hDict