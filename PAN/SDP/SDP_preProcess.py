
import sys
from datetime import datetime
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet
import SDP_aux as aux
import SDP_gene as drv
import SDP_land as lnd


if monet.isNotebook():
    (USR, DRV, AOI) = ('dsk', 'IIT', 'HLT')
    (OVW, JOB) = (True, 4)
else:
    (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
    (OVW, JOB) = (True, 8)
###############################################################################
EXPS = ('000', '001', '010')
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
# Male/Female counts ----------------------------------------------------------
MF = (True, True)
if AOI == 'HLT':
    MF = (False, True)
###############################################################################
# Experiments loop
###############################################################################
exp = EXPS[0]
for exp in EXPS:
    ###########################################################################
    # Setting up paths
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=11000), lnd.landSelector()
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, fldr, exp
    )
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_DTA, PT_PRE, tS, 'SDP Preprocess {} [{}]'.format(DRV, AOI)
    )
    ###########################################################################
    # Load folders
    ###########################################################################
    (expDirsMean, expDirsTrac) = monet.getExpPaths(
        PT_DTA, mean='ANALYZED/', reps='TRACES/'
    )
    (expNum, nodeDigits) = (len(expDirsMean), len(str(len(land)))+1)
    outNames = monet.splitExpNames(PT_OUT)
    outExpNames = set(outNames)
    ###########################################################################
    # Process data
    ###########################################################################
    Parallel(n_jobs=1)(
        delayed(monet.preProcess)(
                exIx, expNum, expDirsMean, expDirsTrac, gene,
                analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
                outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
                MF=MF, cmpr='bz2', nodeDigits=nodeDigits,
                SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
        ) for exIx in range(0, expNum)
    )

