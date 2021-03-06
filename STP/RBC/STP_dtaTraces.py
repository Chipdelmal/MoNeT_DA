
import sys
import compress_pickle as pkl
from os import path
from joblib import dump, load
from datetime import datetime
import pandas as pd
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_auxDebug as dbg
from joblib import Parallel, delayed
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

if monet.isNotebook():
    (USR, LND, AOI, DRV, QNT, TRC) = ('dsk', 'PAN', 'HLT', 'LDR', '50', 'ECO')
else:
    (USR, LND, AOI, DRV, QNT, TRC) = (
        sys.argv[1], sys.argv[2], sys.argv[3], 
        sys.argv[4], sys.argv[5], sys.argv[6]
    )
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
# Experiments -----------------------------------------------------------------
(EXPS, DRV) = (aux.getExps(LND), 'LDR')
exp = EXPS[0]
###############################################################################
# Paths
###############################################################################
EXPS = aux.getExps(LND)
(drive, land) = (
    drv.driveSelector(aux.DRV, TRC, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND)
)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, EXPS[0], LND, DRV)
PT_OUT = path.join(path.split(path.split(PT_ROT)[0])[0], 'ML')
PT_IMG = PT_IMG + 'dtaTraces/'
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_IMG, tS,
    aux.XP_ID+' DtaTraces[{}:{}:{}]'.format(DRV, exp, AOI)
)
###############################################################################
# Read Iter
###############################################################################
expsIter = load(path.join(PT_OUT, 'DTA_PST.job'))
###############################################################################
# Style
###############################################################################
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
    "width": .5, "alpha": .5, "dpi": 300, "legend": True,
    "aspect": 1, "colors": CLR, "xRange": aux.XRAN, "yRange": YRAN
}
###############################################################################
# Plot
###############################################################################
(fNum, digs) = monet.lenAndDigits(expsIter)
Parallel(n_jobs=JOB)(
    delayed(dbg.exportPstTracesParallel)(
        exIx, fNum,
        aux.STABLE_T, 0, QNT, STYLE, PT_IMG, 
        digs=digs, border=True, autoAspect=True, labelPos=(.8, .2)
    ) for exIx in expsIter
)
# Export gene legend ------------------------------------------------------
repDta = pkl.load(expsIter[0][1])
monet.exportGeneLegend(
    repDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
    PT_IMG+'/legend_{}.png'.format(TRC), 500
)
