#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
from glob import glob
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd
import YDR_plots as plt
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
from joblib import Parallel, delayed


if monet.isNotebook():
    (USR, SET, DRV, AOI) = ('dsk', 'homing', 'ASD', 'HLT')
    JOBS = 4
else:
    (USR, SET, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    JOBS = 8
###############################################################################
# Setting up paths and style
###############################################################################
EXPS = aux.EXPS
exp=EXPS[0]
for exp in EXPS:
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
        lnd.landSelector('SPA')
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, SET, fldr, exp
    )
    PT_IMG = PT_IMG + 'preTraces/'
    monet.makeFolder(PT_IMG)
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .3, "alpha": .5, "dpi": 250, "legend": True,
            "aspect": .25, "colors": CLR, "xRange": aux.XRAN, "yRange": YRAN
        }
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    tS = datetime.now()
    monet.printExperimentHead(
        PT_PRE, PT_IMG, tS, aux.XP_ID+' PreTraces {} [{}]'.format(DRV, AOI)
    )
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    tyTag = ('sum', 'srp')
    (fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
    if aux.FZ:
        fltrPattern = PT_PRE + aux.patternForReleases('homing', '00', AOI, '*')
    fLists = monet.getFilteredTupledFiles(fltrPattern, globPattern, tyTag)
    fLists.reverse()
    ###########################################################################
    # Process files
    ###########################################################################
    (xpNum, digs) = monet.lenAndDigits(fLists)
    i = 0
    for i in range(0, xpNum):
        monet.printProgress(i+1, xpNum, digs)
        (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
        name = fLists[i][0].split('/')[-1].split('.')[0][:-4]
        framesPth = PT_IMG + 'videoCache'
        monet.makeFolder(framesPth)
        print('* ' + name, end='\r')
        # Export plots --------------------------------------------------------
        Parallel(n_jobs=JOBS)(
            delayed(monet.exportTracesPlotVideo)(
                repDta, str(day).zfill(5),
                STYLE, framesPth, vLines=[day, aux.XRAN[1]]
            ) for day in range(0, int(aux.XRAN[1]))
        )
        #######################################################################
        # Video
        #######################################################################        
        outPath = PT_IMG + name + '.mp4'
        inPath = framesPth + "/" + '%05d.png'
        sp = subprocess.Popen([
            'ffmpeg', '-y',
            '-loglevel', 'quiet', 
            '-hide_banner',
            '-start_number', '1',
            '-r', str(aux.FRATE),
            '-f', 'image2',
            '-s', '1920x1080',
            '-i', inPath,
            '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
            '-vcodec', 'libx264',
            '-preset', 'veryslow',
            '-crf', '15',
            '-pix_fmt', 'yuv420p',
            outPath
        ])
        sp.wait()
