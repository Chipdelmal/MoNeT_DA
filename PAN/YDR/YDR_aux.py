

import re
import matplotlib
import pandas as pd
# import numpy as np
from glob import glob
import MoNeT_MGDrivE as monet


(XP_HOM, XP_SUP) = (
    'E_{}_{}_{}_{}_{}_{}-{}_{}_{}.{}',
    'E_{}_{}_{}_{}_{}_{}-{}_{}_{}.{}'
)

# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, SET, DRV, EXP):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/yLinked/{}/{}/{}/'.format(SET, DRV, EXP)
    elif USR == 'lap':
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
        cmap = cmapC
    elif AOI == 'TRS':
        cmap = cmapM
    elif AOI == 'WLD':
        cmap = cmapW
    return (scalers, HD_DEP, IND_RAN, cmap)


# def setupFolder(USR, DRV, exp, HD_IND):
#     (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = selectPath(USR, DRV, exp)
#     PT_IMG = PT_IMG[:-1]+'Pst/'
#     fldrName = '{}_{}/'.format(*HD_IND)
#     PT_IMG_XP = PT_IMG+fldrName
#     monet.makeFolder(PT_IMG)
#     monet.makeFolder(PT_IMG_XP)
#     return (PT_ROT, PT_IMG_XP, PT_DTA, PT_PRE, PT_OUT)


def loadDFFromFiles(fName, IND_RAN):
    df = pd.read_csv(fName[0])
    for filename in fName:
        df = df.append(pd.read_csv(filename))
    header = list(df.columns)
    headerInd = header[:IND_RAN]
    return (df, header, headerInd)


def loadDFFromSummary(fName):
    df = pd.read_csv(fName)
    header = list(df.columns)
    indRan = sum([i[0] == 'i' for i in header])
    headerInd = header[:indRan]
    return (df, header, headerInd)

# #############################################################################
# Paths and Names
# #############################################################################
def getExpPaths(PATH_DATA):
    (expDirsMean, expDirsTrac) = (
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'ANALYZED/'),
            monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'TRACE/')
        )
    expDirsMean.sort()
    expDirsTrac.sort()
    return (expDirsMean, expDirsTrac)


def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def getFilteredFiles(filterGlobPattern, unfilteredGlobPattern):
    filterSet = set(glob(filterGlobPattern))
    fullSet = set(glob(unfilteredGlobPattern))
    filteredList = sorted(list(fullSet - filterSet))
    return filteredList

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


def axisRange(x):
    return (min(x), max(x))


# #############################################################################
# Terminal
# #############################################################################
def printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time, title):
    print(monet.PAD)
    (cred, cwht, cend) = (monet.CRED, monet.CWHT, monet.CEND)
    print(cwht+'* MoNeT '+title+' ['+str(time)+']'+cend)
    # print(monet.PAD)
    print('{}* Root: {}{}'.format(cred, PATH_ROOT, cend))
    # print('{}* Imgs: {}{}'.format(cred, PATH_IMG, cend))
    # print('{}* Data: {}{}'.format(cred, PATH_DATA, cend))
    print(monet.PAD)


# #############################################################################
# Color Palette
# #############################################################################
cdict = {
        'red':  ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 0.25, 0.25), (1.0, 0.0, 0.0)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 0.3, 0.3), (1.0, 0.0, 0.0)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 1.0, 1.0), (1.0, 0.25, 0.25))
    }
cmapB = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)
cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.95, 0.95)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0, 0)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.4, 0.4))
    }
cmapC = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)
cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0, 0)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.65, 0.65)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, .95, .95))
    }
cmapM = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)
cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.05, 0.05)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.91, 0.91)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.06, 0.06))
    }
cmapW = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)

# [i/256 for i in (14, 235, 16)]
