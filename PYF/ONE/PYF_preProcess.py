
import sys
import PYF_aux as aux
import PYF_gene as drv
import PYF_land as lnd
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed


if monet.isNotebook():
    (USR, DRV, AOI, LND) = ('dsk', 'PGS', 'HLT', 'PAN')
else:
    (USR, DRV, AOI, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
###############################################################################
(FMT, OVW, JOB, MF) = ('bz2', True, 40, (True, True))
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
###############################################################################
if AOI == 'HLT':
    MF = (False, True)
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR, PT_MOD) = aux.selectPath(
    USR, LND
)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_DTA, PT_PRE, tS, 'PYF Preprocess ' + AOI)
###############################################################################
# Load landscape and drive
###############################################################################
drive = drv.driveSelector(DRV, AOI, popSize=20*62)
land = lnd.landSelector(LND, PT_ROT)
gene = drive.get('gDict')
###############################################################################
# Load folders
###############################################################################
(expDirsMean, expDirsTrac) = monet.getExpPaths(
    PT_DTA, mean='ANALYZED/', reps='TRACE/'
)
(expNum, nodeDigits) = (len(expDirsMean), len(str(len(land)))+1)
done = set(aux.splitExpNames(PT_PRE))
###############################################################################
# Analyze data
###############################################################################
Parallel(n_jobs=JOB)(
    delayed(monet.preProcess)(
            exIx, expNum, expDirsMean, expDirsTrac, gene,
            analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
            outExpNames=done, fNameFmt='{}/{}-{}_', OVW=OVW,
            MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
            SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
    ) for exIx in range(0, expNum)
)
