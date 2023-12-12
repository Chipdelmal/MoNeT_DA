import sys
from os import path
from joblib import load
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import TPP_aux as aux
import TPP_gene as drv
import warnings
warnings.filterwarnings("ignore")

if monet.isNotebook():
    (USR, LND, EXP, DRV, AOI, QNT, THS, TRC) = (
        'zelda', 'Kenya', 'highEIR', 'LDR', 'HLT', '50', '0.1', 'HLT'
    )
else:
    (USR, LND, EXP, DRV, AOI, QNT, THS, TRC) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'zelda':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###########################################################################
# Paths
###########################################################################
(NH, NM) = aux.getPops(LND)
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=NM, humSize=0),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, EXP)
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
CLR = drive.get('colors')
if DRV != 'HUM':
    YRAN = drive.get('yRange')
else:
    YRAN = aux.getHumanRange(AOI)
STYLE = {
    "width": 0.5, "alpha": .005, "dpi": 750, "aspect": 1/5, 
    "colors": CLR, "legend": True,
    "xRange": aux.XRAN, "yRange": (0, YRAN)
}
STYLE['aspect'] = monet.scaleAspect(0.3, STYLE)
###############################################################################
# Plot
###############################################################################
(fNum, digs) = monet.lenAndDigits(subset)
Parallel(n_jobs=JOB)(
    delayed(aux.exportPstTracesParallel)(
        exIx, fNum,
        aux.STABLE_T, 0, QNT, STYLE, pt_img,
        digs=digs, border=True, autoAspect=False, labelPos=(.01, .925),
        wopPrint=True, mnfPrint=True, cptPrint=True, 
        poePrint=False, ttiPrint=True, ttoPrint=True,
        labelspacing=.05,
        ticksHide=False,
        transparent=True, sampRate=aux.SAMP_RATE,
        releases=[aux.REL_START+1],
        hLines=[aux.POP_SIZE, aux.POP_SIZE/2]
    ) for exIx in subset
)