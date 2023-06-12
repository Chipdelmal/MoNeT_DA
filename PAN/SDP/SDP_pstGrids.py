
import cv2
import sys
from glob import glob
from datetime import datetime
import SDP_aux as aux
import SDP_gene as drv
import SDP_land as lnd
import MoNeT_MGDrivE as monet
from cv2 import imread, imwrite, hconcat, vconcat


if monet.isNotebook():
    (USR, DRV, QNT) = ('dsk', 'SDR', '50')
else:
    (USR, DRV, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3])
(AOI, EXPS) = (aux.DATA_PST, aux.EXPS)
exp=EXPS[0]
for exp in EXPS:
    # #########################################################################
    # Setup paths and drive
    # #########################################################################
    (drive, land) = (drv.driveSelector(DRV, AOI[0]), lnd.landSelector())
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, fldr, exp
    )
    (PT_IMG_I, PT_IMG_O) = (PT_IMG + 'pstTraces/', PT_IMG + 'pstGrids/')
    monet.makeFolder(PT_IMG_O)
    tS = datetime.now()
    monet.printExperimentHead(PT_IMG_I, PT_IMG_O, tS, 'PstGrids {}'.format(DRV))
    # Get files ---------------------------------------------------------------
    NODE_NUM = len(land)
    imgLists = [
        glob('{}E_*{}*{}*{}.png'.format(PT_IMG_I, i, '*', QNT)) for i in AOI
    ]
    imgTuples = list(zip(*[sorted(i) for i in imgLists]))
    imgChunks = list(monet.divideListInChunks(imgTuples, NODE_NUM))[:-1]
    # #########################################################################
    # Iterate through images
    # #########################################################################
    (xpNum, digs) = monet.lenAndDigits(imgChunks)
    for (i, chunk) in enumerate(imgChunks):
        monet.printProgress(i+1, xpNum, digs)
        expGrid = vconcat([hconcat([imread(i, cv2.IMREAD_UNCHANGED) for i in j]) for j in chunk])
        # [[imread(i).shape for i in j] for j in chunk]
        fName = chunk[0][0].split('/')[-1].split('-')[0] + '-' + QNT
        imwrite(PT_IMG_O + fName + '.png', expGrid)