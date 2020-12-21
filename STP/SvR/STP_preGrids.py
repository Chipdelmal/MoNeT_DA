#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
from cv2 import imread, imwrite, hconcat, vconcat


# (USR, REL, LND) = (sys.argv[1], sys.argv[2], sys.argv[3])
(USR, REL, LND) = ('dsk', 'mixed', 'PAN')
(DRV, FMT, OVW, FZ) = ('LDR', 'bz2', True, True)
AOI = ['ECO', 'HLT', 'TRS', 'WLD']
###########################################################################
# Setting up paths and style
###########################################################################
# Paths -------------------------------------------------------------------
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
monet.makeFolder(PT_IMG)
# Drive and land selector -------------------------------------------------
(drive, land) = (
    drv.driveSelector(DRV, AOI[0], popSize=100*12000),  
    lnd.landSelector(LND, REL, PT_ROT)
)
# #########################################################################
# Setup paths and drive
# #########################################################################
(drive, land) = (drv.driveSelector(DRV, AOI[0]), lnd.landSelector('SPA'))
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_IMG_I, PT_IMG_O) = (PT_IMG + 'preTraces/', PT_IMG + 'preGrids/')
monet.makeFolder(PT_IMG_O)
tS = datetime.now()
monet.printExperimentHead(PT_IMG_I, PT_IMG_O, tS, 'UCIMI Grids ')
# Get files ---------------------------------------------------------------
NODE_NUM = len(land)
imgLists = [glob('{}*{}*{}*'.format(PT_IMG_I, i, '*')) for i in AOI]
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