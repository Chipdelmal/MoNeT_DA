
import sys
from glob import glob
from datetime import datetime
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd
import MoNeT_MGDrivE as monet
from cv2 import imread, imwrite, hconcat, vconcat


# (USR, SET, DRV) = ('dsk', 'homing', 'ASD')
(USR, SET, DRV) = (sys.argv[1], sys.argv[2], sys.argv[3])
(FMT, SKP, FZ) = ('bz2', False, False)
AOI = ['ECO', 'HLT', 'TRS', 'WLD']
EXPS = ('000', '002', '004', '006', '008')
for EXP in EXPS:
    # #########################################################################
    # Setup paths and drive
    # #########################################################################
    (drive, land) = (drv.driveSelector(DRV, AOI[0]), lnd.landSelector('SPA'))
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, EXP
    )
    (PT_IMG_I, PT_IMG_O) = (PT_IMG + 'preTraces/', PT_IMG + 'preGrids/')
    monet.makeFolder(PT_IMG_O)
    tS = datetime.now()
    monet.printExperimentHead(PT_IMG_I, PT_IMG_O, tS, 'Grids ')
    # Get files ---------------------------------------------------------------
    NODE_NUM = len(land)
    imgLists = sorted([glob('{}*{}*{}*'.format(PT_IMG_I, i, '*')) for i in AOI])
    imgTuples = list(zip(*[sorted(i) for i in imgLists]))
    imgChunks = list(aux.divideChunks(imgTuples, NODE_NUM))[:-1]
    # #########################################################################
    # Iterate through images
    # #########################################################################
    (xpNum, digs) = monet.lenAndDigits(imgChunks)
    for (i, chunk) in enumerate(imgChunks):
        monet.printProgress(i+1, xpNum, digs)
        expGrid = vconcat([hconcat([imread(i) for i in j]) for j in chunk])
        fName = chunk[0][0].split('/')[-1].split('-')[0]
        imwrite(PT_IMG_O + fName + '.png', expGrid)