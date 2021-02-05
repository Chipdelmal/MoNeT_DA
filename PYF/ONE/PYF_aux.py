

import re
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
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)


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
    print(XP_PAT.format(*patList))
    return XP_PAT.format(*patList)

