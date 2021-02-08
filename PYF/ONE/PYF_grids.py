
import sys
from os import path
from glob import glob
from datetime import datetime
import PYF_aux as aux
import PYF_gene as drv
import PYF_land as lnd
import MoNeT_MGDrivE as monet
from cv2 import imread, imwrite, hconcat, vconcat


if monet.isNotebook():
    (USR, DRV, AOI, LND, STG) = ('dsk', 'PGS', 'HLT', 'SPA', 'PRE')
else:
    (USR, DRV, AOI, LND, STG) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
###############################################################################
(FMT, SKP, FZ) = ('bz2', False, False)
AOI = ['HLT']
# #############################################################################
# Setup paths and drive
# #############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR, PT_MOD) = aux.selectPath(
    USR, LND
)
if STG == 'PRE':
    (PT_IMG_I, PT_IMG_O) = (
        path.join(PT_IMG, 'preTraces/'), path.join(PT_IMG, 'preGrids/')
    )
else:
    (PT_IMG_I, PT_IMG_O) = (
        path.join(PT_IMG, 'pstTraces/'), path.join(PT_IMG, 'pstGrids/')
    )
drive = drv.driveSelector(DRV, AOI[0], popSize=20*62)
land = lnd.landSelector(LND, PT_ROT)
monet.makeFolder(PT_IMG_O)
# #############################################################################
# Get Files
# #############################################################################
tS = datetime.now()
monet.printExperimentHead(PT_IMG_I, PT_IMG_O, tS, 'Grids ')
# Get files -------------------------------------------------------------------
NODE_NUM = len(land)
imgLists = [glob('{}*{}*{}*'.format(PT_IMG_I, i, '*')) for i in AOI]
imgTuples = list(zip(*[sorted(i) for i in imgLists]))
imgChunks = list(monet.divideListInChunks(imgTuples, NODE_NUM))[:-1]
# #############################################################################
# Iterate through images
# #############################################################################
(xpNum, digs) = monet.lenAndDigits(imgChunks)
for (i, chunk) in enumerate(imgChunks):
    monet.printProgress(i+1, xpNum, digs)
    expGrid = hconcat([vconcat([imread(i) for i in j]) for j in chunk])
    fName = chunk[0][0].split('/')[-1].split('-')[0]
    imwrite(PT_IMG_O + fName + '.png', expGrid)
