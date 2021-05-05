
import sys
from glob import glob
from datetime import datetime
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd
import MoNeT_MGDrivE as monet
from cv2 import imread, imwrite, hconcat, vconcat

if monet.isNotebook():
    (USR, SET, DRV, QNT) = ('dsk', 'homing', 'ASD', '50')
else:
    (USR, SET, DRV, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
(AOI, EXPS) = (aux.DATA_PST, aux.EXPS)
exp = EXPS[0]
for exp in EXPS:
    # #########################################################################
    # Setup paths and drive
    # #########################################################################
    (drive, land) = (drv.driveSelector(DRV, AOI[0]), lnd.landSelector('SPA'))
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, exp
    )
    PT_IMG_P = PT_IMG+'preTraces/'
    (PT_IMG_I, PT_IMG_O) = (PT_IMG + 'pstTraces/', PT_IMG + 'pstGrids/')
    monet.makeFolder(PT_IMG_O)
    tS = datetime.now()
    monet.printExperimentHead(
        PT_IMG_I, PT_IMG_O, tS, 
        aux.XP_ID+' PstGrids [{}:{}]'.format(DRV, exp)
    )
    # Get files ---------------------------------------------------------------
    NODE_NUM = len(land)
    imgListPre = sorted(glob('{}*E*{}*{}*.png'.format(PT_IMG_P, 'ECO', '*')))
    imgLists = [
        sorted(glob('{}E_*{}*{}*{}.png'.format(PT_IMG_I, i, '*', QNT))) 
            for i in AOI
    ]
    if len(imgListPre) == len(imgLists[0]):
        imgLists.append(imgListPre)
        for i in range(len(imgListPre)):
            imgLists = imgLists[-1:] + imgLists[:-1]
    imgTuples = list(zip(*[sorted(i) for i in imgLists]))
    imgChunks = list(monet.divideListInChunks(imgTuples, NODE_NUM))[:]
    # #########################################################################
    # Iterate through images
    # #########################################################################
    (xpNum, digs) = monet.lenAndDigits(imgChunks)
    for (i, chunk) in enumerate(imgChunks):
        monet.printProgress(i+1, xpNum, digs)
        expGrid = vconcat([hconcat([imread(i) for i in sorted(j)]) for j in chunk])
        fName = chunk[0][0].split('/')[-1].split('-')[0] + '-' + QNT
        imwrite(PT_IMG_O + fName + '.png', expGrid)