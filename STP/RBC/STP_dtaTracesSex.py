
import sys
from os import path
from glob import glob
from datetime import datetime
from cv2 import imread, imwrite, hconcat, vconcat
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd



if monet.isNotebook():
    (USR, LND, AOI, QNT) = ('dsk', 'PAN', 'HLT', '50')
else:
    (USR, LND, AOI, QNT) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
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
(drive, land) = (
    drv.driveSelector(aux.DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(EXPS[0], LND)
)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, EXPS[0], LND)
PT_OUT = path.join(path.split(path.split(PT_ROT)[0])[0], 'ML')
PT_IMG = PT_IMG + 'dtaTraces/'
PT_IMG_O = PT_IMG + 'dtaGridsSex/'
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG, PT_IMG_O]]
PT_SUMS = [path.join(PT_ROT, exp, 'SUMMARY') for exp in EXPS]
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_IMG, tS,
    aux.XP_ID+' DtaTracesStack[{}:{}:{}]'.format(DRV, exp, AOI)
)
# Get files ---------------------------------------------------------------
NODE_NUM = len(land)
imgListA = sorted(glob('{}*E_01*{}*.png'.format(PT_IMG, AOI, '*')))
imgListB = sorted(glob('{}*E_02*{}*.png'.format(PT_IMG, AOI, '*')))
imgTuples = list(zip(imgListA, imgListB))
imgChunks = list(monet.divideListInChunks(imgTuples, NODE_NUM))[:]
# #########################################################################
# Iterate through images
# #########################################################################
(xpNum, digs) = monet.lenAndDigits(imgChunks)
for (i, chunk) in enumerate(imgChunks):
    monet.printProgress(i+1, xpNum, digs)
    expGrid = vconcat(
        [hconcat([imread(i) for i in sorted(j)]) for j in chunk]
    )
    fName = chunk[0][0].split('/')[-1].split('-')[0]
    imwrite(PT_IMG_O + fName + '.png', expGrid)