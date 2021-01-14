

import MoNeT_MGDrivE as monet

# #############################################################################
# Paths
# #############################################################################
def selectPath(USR, LND, EXP):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/PYF/{}/{}/'.format(LND, EXP)
    else:
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/PYF/{}/{}/'.format(LND, EXP)
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)