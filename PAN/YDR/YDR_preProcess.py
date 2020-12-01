
import sys
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed


(USR, SET, DRV, AOI) = ('lap', 'homing', 'XSD', 'HLT')
# (USR, EXP, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
(FMT, OVW, MF, JOB) = ('bz2', True, (False, True), 8)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
EXPS = ('000', '002', '004', '006', '008')
for EXP in EXPS:
    ###########################################################################
    # Setting up paths and style
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=11000),
        lnd.landSelector('SPA')
    )
    gene = drive.get('gDict')
    fldr = drive.get('folder')
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, EXP
    )
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    aux.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Preprocess ' + AOI)
    ###########################################################################
    # Load folders
    ###########################################################################
    (expDirsMean, expDirsTrac) = aux.getExpPaths(PT_DTA)
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
                MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
                SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
        ) for exIx in range(0, expNum)
    )

drive