
import sys
import compress_pickle as pkl
from os import path
from joblib import dump, load
from datetime import datetime
import pandas as pd
import MoNeT_MGDrivE as monet
import tGD_aux as aux
import tGD_gene as drv
from joblib import Parallel, delayed
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

if monet.isNotebook():
    (USR, DRV) = (
        'srv', 'linkedDrive'
    )
else:
    (USR, DRV, AOI, QNT, THS, TRC) = sys.argv[1:]
(AOI, QNT, THS, TRC) = (('HLT', 'TRS'), '50', '0.1', 'HLT')
TICKS_HIDE = True
# Setup number of cores -------------------------------------------------------
JOB = aux.JOB_DSK
if USR=='srv':
    JOB = aux.JOB_SRV
# Experiments -----------------------------------------------------------------
exp =aux.EXPS[0]
###############################################################################
# Paths
###############################################################################
land = [[0], ]
driveA = drv.driveSelector(DRV, AOI[0], popSize=aux.POP_SIZE)
driveB = drv.driveSelector(DRV, AOI[1], popSize=aux.POP_SIZE)
(gene, fldr) = (driveA.get('gDict'), driveA.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = PT_IMG + 'dtaTraces/'
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, '100', 'SUMMARY')
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_IMG, tS,
    'tGD'+' DtaTraces [{}:{}:{}]'.format(DRV, exp, AOI)
)
###############################################################################
# Read Iter
###############################################################################
expsIterA = load(path.join(PT_OUT, 'DTA_PST_{}.job'.format(AOI[0])))
expsIterB = load(path.join(PT_OUT, 'DTA_PST_{}.job'.format(AOI[1])))
###############################################################################
# Subset by Folder
###############################################################################
pt_root = PT_ROT
for (i, expsIter) in enumerate([expsIterA, expsIterB]):
    subset = [exp for exp in expsIter if exp[1].find(pt_root)==0]
    drive = drv.driveSelector(DRV, AOI[i], popSize=aux.POP_SIZE)
    ###########################################################################
    # Style
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
        "width": .5, "alpha": .9, "dpi": 200, "legend": True,
        "aspect": .5, "colors": CLR, "xRange": aux.XRAN,
        "yRange": (0, YRAN[1]*2.5)
    }
    STYLE['aspect'] = monet.scaleAspect(1/4, STYLE)
    # print('YRAN: {}'.format(STYLE))
    ###########################################################################
    # Plot
    ###########################################################################
    (fNum, digs) = monet.lenAndDigits(subset)
    Parallel(n_jobs=JOB)(
        delayed(aux.exportPstTracesParallel)(
            exIx, fNum,
            0, 0, QNT, STYLE, PT_IMG,
            digs=digs, border=True, autoAspect=False, labelPos=(.8, .15),
            poePrint=False, ticksHide=TICKS_HIDE, labelspacing=.05,
            mnfPrint=False,
            transparent=False, sampRate=aux.SAMP_RATE
        ) for exIx in subset
    )
    # Export gene legend ------------------------------------------------------
# repDta = pkl.load(expsIter[0][1])
# monet.exportGeneLegend(
#     repDta['genotypes'], [i[:-2]+'cc' for i in CLR], 
#     PT_IMG+'/legend_{}.png'.format(TRC), 500
# )
