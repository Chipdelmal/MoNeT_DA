#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
from glob import glob
import time
from os import path
from sys import argv
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import tGD_aux as aux
import tGD_fun as fun
import tGD_gene as drv
import tGD_plots as plots
import MoNeT_MGDrivE as monet

(USR, DRV) = (sys.argv[1], sys.argv[2])
# (USR, DRV) = ('dsk', 'splitDrive')
(FMT, SKP, MF, FZ) = ('bz2', False, (True, True), False)
EXP = aux.EXPS
typs = ('CST', 'HLT')
DPI = 300
AOI = 'HLT'
##############################################################################
# Setting up paths and style
###############################################################################
exp = EXP[0]
for exp in EXP:
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
    PT_IMG_I = PT_IMG + 'preTraces/'
    PT_IMG_O = PT_IMG + 'preOverlay/'
    monet.makeFolder(PT_IMG_O)
    drive = drv.driveSelector(DRV, AOI)
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .25, "alpha": .75, "dpi": 750, "legend": True,
            "aspect": .25, "colors": CLR, "xRange": [0, (365*5)/3],
            "yRange": (0, YRAN[1]*1.5)
        }
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    tS = datetime.now()
    aux.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'PreOverlays '+AOI)
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    fLists = list(zip(
        *[sorted(glob(PT_IMG_I+'*'+'*'+tp+'*')) for tp in typs]
    ))
    ###########################################################################
    # Iterate file lists
    ###########################################################################
    for fs in fLists:
        imgs = [Image.open(i).convert('RGBA') for i in fs]
        (w, h) = imgs[0].size
        bkg = Image.new('RGBA', (w, h), (255, 255, 255, 255))
        for i in imgs:
            bkg.paste(i, (0, 0), i)
            i.close()
        bkg.save(PT_IMG_O+fs[0].split('/')[-1], dpi=(DPI, DPI))
        bkg.close()

