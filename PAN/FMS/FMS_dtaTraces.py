import sys
from os import path
import pandas as pd
from glob import glob
from joblib import load
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import FMS_aux as aux
import FMS_gene as drv

if monet.isNotebook():
    (USR, DRV, QNT, AOI) = ('srv', 'PGS', '50', 'HLT')
else:
    (USR, DRV, QNT, AOI) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###########################################################################
# Paths
###########################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, fldr)
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
###############################################################################
# Read Iter
###############################################################################
expsIter = load(path.join(PT_OUT, 'DTA_PST_{}.job'.format(AOI)))
expsIter = [i for i in expsIter if len(i) > 0]
###############################################################################
# Subset by Folder
###############################################################################
pt_img = path.join(PT_ROT, 'img', 'dtaTraces')
monet.makeFolder(pt_img)
subset = [exp for exp in expsIter if exp[1].find(PT_ROT)==0]
# Time and head -----------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_SUMS, pt_img, tS, 
    '{} DtaTraces [{}:{}:{}]'.format('FMS', DRV, QNT, AOI)
)
###############################################################################
# Style
###############################################################################
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
    "width": .1, "alpha": .1, "dpi": 750, "aspect": 1/6, 
    "colors": CLR, "legend": True,
    "xRange": aux.XRAN, "yRange": (0, YRAN[1]*1.5)
}
STYLE['aspect'] = monet.scaleAspect(1.5, STYLE)
###############################################################################
# Plot
###############################################################################
(fNum, digs) = monet.lenAndDigits(subset)
Parallel(n_jobs=JOB)(
    delayed(aux.exportPstTracesParallel)(
        exIx, fNum,
        aux.STABLE_T, 0, QNT, STYLE, pt_img,
        digs=digs, border=True, autoAspect=True, labelPos=(.8, .15),
        poePrint=False, mnfPrint=False, ticksHide=False,
        transparent=True, sampRate=aux.SAMP_RATE
    ) for exIx in subset
)