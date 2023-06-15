import sys
from os import path
from joblib import load
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed
import SDP_aux as aux
import SDP_gene as drv
import SDP_land as lnd
import warnings
warnings.filterwarnings("ignore")

if monet.isNotebook():
    (USR, DRV, AOI, QNT, THS, TRC) = (
        'zelda', 'PGS', 'HLT', '50', '0.1', 'HLT'
    )
else:
    (USR, DRV, AOI, QNT, THS, TRC) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###########################################################################
# Paths
###########################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE), lnd.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
###############################################################################
# Iterate through experiments
###############################################################################
EXPS = aux.EXPS
exp = EXPS[0]
for exp in EXPS:
    ###########################################################################
    # Setting up paths
    ###########################################################################
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, fldr, exp
    )
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
    if DRV != 'HUM':
        (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    else:
        if AOI[:3] == 'MRT':
            (CLR, YRAN) = (drive.get('colors'), (0, 0.5e-5))
        else:
            (CLR, YRAN) = (drive.get('colors'), (0, 1e-2))
    STYLE = {
        "width": 0.25, "alpha": .0005, "dpi": 750, "aspect": 1/5, 
        "colors": CLR, "legend": True,
        "xRange": aux.XRAN, "yRange": (0, YRAN[1]*10)
    }
    ###############################################################################
    # Plot
    ###############################################################################
    (fNum, digs) = monet.lenAndDigits(subset)
    Parallel(n_jobs=JOB)(
        delayed(aux.exportPstTracesParallel)(
            exIx, fNum,
            aux.STABLE_T, 0, QNT, STYLE, pt_img,
            digs=digs, border=True, autoAspect=True, labelPos=(.8, .15),
            wopPrint=False, poePrint=False, mnfPrint=False, cptPrint=False,
            ticksHide=True,
            transparent=True, sampRate=aux.SAMP_RATE,
            releases=[
                aux.REL_START+i*7 for i in 
                range(int(exIx[1].split('/')[-1].split('_')[1]))
            ],
            hLines=[aux.POP_SIZE, aux.POP_SIZE/2]
        ) for exIx in subset
    )