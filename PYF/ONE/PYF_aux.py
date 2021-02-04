

import MoNeT_MGDrivE as monet

# #############################################################################
# Paths
# #############################################################################
def selectPath(USR, LND):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/PYF/{}/'.format(LND)
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


