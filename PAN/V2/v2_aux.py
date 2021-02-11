

import MoNeT_MGDrivE as monet

# #############################################################################
# Paths
# #############################################################################
def selectPath(USR):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/mgdrive2_paper/'
    else:
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/v2/Reviewers/'
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)