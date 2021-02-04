
import sys
import PYF_aux as aux
import PYF_gene as drv
import PYF_land as lnd
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed


(USR, DRV, AOI, LND) = ('dsk', 'PGS', 'HLT', 'PAN')
###############################################################################
(FMT, OVW, JOB, MF) = ('bz2', True, 16, (True, True))
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
###############################################################################
if AOI == 'HLT':
    MF = (False, True)
###############################################################################
# Setting up paths and style
###############################################################################
drive = drv.driveSelector(DRV, AOI, popSize=11000)
land = lnd.landSelector('SPA')
gene = drive.get('gDict')
fldr = drive.get('folder')
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_DTA, PT_PRE, tS, 'Preprocess ' + AOI)
###########################################################################
# Load folders
###########################################################################
(expDirsMean, expDirsTrac) = monet.getExpPaths(
    PT_DTA, mean='ANALYZED/', reps='TRACE/'
)
(expNum, nodeDigits) = (len(expDirsMean), len(str(len(land)))+1)
# outNames = aux.splitExpNames(PT_OUT)
# outExpNames = set(outNames)