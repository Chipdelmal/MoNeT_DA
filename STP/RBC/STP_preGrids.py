
import sys
from glob import glob
from datetime import datetime
from cv2 import imread, imwrite, hconcat, vconcat
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd


if monet.isNotebook():
    (USR, LND) = ('dsk', 'PAN')
    JOB = aux.JOB_DSK
else:
    (USR, LND) = (sys.argv[1], sys.argv[2])
    JOB = aux.JOB_SRV
(AOI, EXPS, DRV) = (aux.DATA_PRE, aux.getExps(LND), 'LDR')
exp = EXPS[0]
for exp in EXPS:
    # #########################################################################
    # Setup paths and drive
    # #########################################################################
    (drive, land) = (
        drv.driveSelector(aux.DRV, AOI[0], popSize=aux.POP_SIZE),
        lnd.landSelector(exp, LND)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, LND
    )
    (PT_IMG_I, PT_IMG_O) = (PT_IMG+'preTraces/', PT_IMG+'preGrids/')
    monet.makeFolder(PT_IMG_O)
    tS = datetime.now()
    monet.printExperimentHead(
        PT_IMG_I, PT_IMG_O, tS, aux.XP_ID+' PreGrids [{}:{}]'.format(DRV, exp)
    )
    # Get files ---------------------------------------------------------------
    NODE_NUM = len(land)
    imgLists = [glob('{}*{}*{}*.png'.format(PT_IMG_I, i, '*')) for i in AOI]
    imgTuples = list(zip(*[sorted(i) for i in imgLists]))
    imgChunks = list(monet.divideListInChunks(imgTuples, NODE_NUM))[:-1]
    # #########################################################################
    # Iterate through images
    # #########################################################################
    (xpNum, digs) = monet.lenAndDigits(imgChunks)
    for (i, chunk) in enumerate(imgChunks):
        monet.printProgress(i+1, xpNum, digs)
        expGrid = vconcat([hconcat([imread(i) for i in j]) for j in chunk])
        fName = chunk[0][0].split('/')[-1].split('-')[0]
        imwrite(PT_IMG_O + fName + '.png', expGrid)