#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PIL import Image
from datetime import datetime
import MoNeT_MGDrivE as monet
from glob import glob
from os import path
import compress_pickle as pkl
import TPT_aux as aux
import TPT_gene as drv


if monet.isNotebook():
    (USR, AOI, DRV) = ('dsk', 'HLT', 'LDR')
else:
    (USR, AOI, DRV) = (sys.argv[1], sys.argv[2], sys.argv[3])
patterns = ('*HLT_*', '*HUM_*')
# Setup number of threads -----------------------------------------------------
JOB=aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
###############################################################################
# Processing loop
###############################################################################
EXPS = aux.getExps()
exp = EXPS[0]
for exp in EXPS:
    ###########################################################################
    # Setting up paths
    ###########################################################################
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE, humSize=aux.HUM_SIZE),
        aux.landSelector(USR=USR)
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, exp, DRV
    )
    PT_IMG = path.join(PT_IMG, 'preTraces')
    # Time and head -----------------------------------------------------------
    (expDirsMean, expDirsTrac) = monet.getExpPaths(
        PT_DTA, mean='ANALYZED/', reps='TRACE/'
    )
    ###########################################################################
    # Setting up paths
    ###########################################################################
    pats = list(zip(*[sorted(glob(path.join(PT_IMG, i))) for i in patterns]))
    # Iteration cycle ---------------------------------------------------------
    for fnames in pats:
        background = Image.open(fnames[0])
        whiteBkg = Image.new("RGBA", background.size, "WHITE")
        for i in range(0, len(fnames)):
            foreground = Image.open(fnames[i])
            whiteBkg.paste(foreground, (0, 0), foreground)
            foreground.close()
        (expName, tail) = fnames[0].split('/')[-1].split('-')
        pthSave = path.join(PT_IMG, '{}-INF_{}'.format(expName, tail[4:]))
        whiteBkg.save(pthSave, dpi=(300, 300))
        whiteBkg.close()
