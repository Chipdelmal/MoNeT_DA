
import sys
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed


if monet.isNotebook():
    (USR, SET, DRV, AOI) = ('dsk', 'homing', 'ASD', 'HLT')
    (OVW, JOB) = (True, 4)
else:
    (USR, SET, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    (OVW, JOB) = (True, 8)
###############################################################################
MF = (True, True)
if AOI == 'HLT':
    MF = (False, True)
###############################################################################
EXPS = aux.EXPS
for EXP in EXPS:
    ###########################################################################
    # Setting up paths and style
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE), 
        lnd.landSelector('SPA')
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, EXP
    )
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_DTA, PT_PRE, tS, aux.XP_ID+' PreProcess {} [{}]'.format(DRV, AOI)
    )
    ###########################################################################
    # Load folders
    ###########################################################################
    (expDirsMean, expDirsTrac) = monet.getExpPaths(
        PT_DTA, mean='ANALYZED/', reps='TRACE/'
    )
    (expNum, nodeDigits) = (len(expDirsMean), len(str(len(land)))+1)
    outNames = aux.splitExpNames(PT_OUT)
    outExpNames = set(outNames)
    ###########################################################################
    # Analyze data
    ###########################################################################
    Parallel(n_jobs=JOB)(
        delayed(monet.preProcess)(
                exIx, expNum, expDirsMean, expDirsTrac, gene,
                analysisOI=AOI, prePath=PT_PRE, nodesAggLst=land,
                outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
                MF=MF, cmpr='bz2', nodeDigits=nodeDigits,
                SUM=aux.SUM, AGG=aux.AGG, SPA=aux.SPA,
                REP=aux.REP, SRP=aux.SRP
        ) for exIx in range(0, expNum)
    )
