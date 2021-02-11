

import re
from os import path
from glob import glob
import MoNeT_MGDrivE as monet


XP_PAT = 'E_{}_{}_{}_{}_{}-{}_{}_{}.{}'

# #############################################################################
# Paths
# #############################################################################
def selectPath(USR, LND):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/pyf/{}/'.format(LND)
    else:
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/PYF/Onetahi/sims/{}/'.format(LND)
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = path.join(PATH_DATA, 'PREPROCESS/')
    PATH_OUT = path.join(PATH_DATA, 'POSTPROCESS/')
    PATH_MTR = path.join(PATH_DATA, 'SUMMARY/')
    PATH_MOD = path.join(PATH_DATA, 'MODELS')
    fldrList = [
        PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR, PATH_MOD
    ]
    [monet.makeFolder(i) for i in fldrList]
    return fldrList


# #############################################################################
# Dependent Variables for Heatmaps
# #############################################################################
def selectDepVars(MOI, AOI):
    # Select ranges and dependent variable-------------------------------------
    if (MOI == 'WOP') or (MOI == 'TTI') or (MOI == 'TTO'):
        scalers = [100, 100, round(1800)]
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
# Filenames
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


def patternForReleases(ren, AOI, ftype, ext='bz'):
    patList = ['*', ren, '*', '*', '*', AOI, '*', ftype, ext]
    return XP_PAT.format(*patList)


def getXpId(pFile, idIx):
    splitXpId = re.split('_|-', pFile.split('/')[-1].split('.')[-2])
    xpId = [int(splitXpId[i]) for i in idIx]
    return xpId


