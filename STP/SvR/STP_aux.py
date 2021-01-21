#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import matplotlib
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet


XP_NPAT = 'E_{}_{}_{}_{}_{}-{}_{}_{}.{}'


def humanSelector(AOI, DRV, MGV):
    (drive, mgversion) = (DRV, MGV)
    if AOI == 'HUM':
        (drive, mgversion) = ('HUM', 'v2')
    return (drive, mgversion)


def patternForReleases(ren, AOI, ftype):
    strPat = XP_NPAT.format('*', ren, '*', '*', '*', AOI, '*', ftype, 'bz')
    return strPat


def selectVersionPath(MGV, PT_DTA):
    if MGV == 'v2':
        (expDirsMean, expDirsTrac) = monet.getExpPaths(
            PT_DTA, mean='analyzed/', reps='traces/'
        )
    else:
        (expDirsMean, expDirsTrac) = monet.getExpPaths(
            PT_DTA, mean='ANALYZED/', reps='GARBAGE/'
        )
    return (expDirsMean, expDirsTrac)

# #############################################################################
# Dependent Variables for Heatmaps
# #############################################################################
def selectDepVars(MOI, AOI):
    # Select ranges and dependent variable-------------------------------------
    if (MOI == 'WOP') or (MOI == 'TTI') or (MOI == 'TTO'):
        scalers = [1, 1, round(10*365)]
        (HD_DEP, IND_RAN) = ('0.1', 7)
    elif (MOI == 'RAP'):
        scalers = [1, 100, 1]
        (HD_DEP, IND_RAN) = ('486', 7)
    elif (MOI == 'MNX'):
        scalers = [1, 100, 1]
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


# #############################################################################
# Paths
# #############################################################################
def selectPath(USR, LND, EXP):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/STP/{}/sim/{}/'.format(LND, EXP)
    else:
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/STP/{}/{}/'.format(LND, EXP)
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    if EXP[-1] == 'P':
        PATH_DATA = PATH_DATA[:-2] + '/'
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)

