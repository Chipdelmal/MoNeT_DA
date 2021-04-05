#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
from glob import glob
import PYF_aux as aux
import PYF_gene as drv
import PYF_land as lnd
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
from joblib import Parallel, delayed

if monet.isNotebook():
    (USR, DRV, AOI, LND, EXP) = (
        'dsk', 'PGS', 'HLT', 'PAN', 'E_016_024_100_000_000'
    )
    JOBS = 4
else:
    (USR, DRV, AOI, LND, EXP) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
    JOBS = 8
(FZ, tStable) = (False, int(30/2))
###############################################################################
# Setting up paths
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR, PT_MOD) = aux.selectPath(
    USR, LND
)
PT_IMG = PT_IMG + 'preTraces/'
monet.makeFolder(PT_IMG)
###############################################################################
# Load landscape and drive
###############################################################################
drive = drv.driveSelector(DRV, AOI, popSize=20*62)
land = lnd.landSelector(LND, PT_ROT)
gene = drive.get('gDict')
###############################################################################
# Style 
###############################################################################
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": .2, "alpha": .5, "dpi": 300, "legend": True,
        "aspect": .25, "colors": CLR, "xRange": [0, (365*2.5)],
        "yRange": YRAN
    }
tS = datetime.now()
monet.printExperimentHead(PT_PRE, PT_IMG, tS, 'PYF PreTraces ' + AOI)
###############################################################################
# Process files
###############################################################################
fLists = glob(PT_PRE+EXP+'*'+AOI+'*srp.bz')
(xpNum, digs) = monet.lenAndDigits(fLists)
i=0
for i in range(0, len(fLists)):
    monet.printProgress(i+1, xpNum, digs)
    repDta = pkl.load(fLists[i])
    name = fLists[i].split('/')[-1].split('/')[-1].split('.')[0][:-4]
    framesPth = PT_IMG + 'videoCache'
    monet.makeFolder(framesPth)
    print('* ' + name, end='\r')
    # Export plots --------------------------------------------------------
    Parallel(n_jobs=JOBS)(
        delayed(monet.exportTracesPlotVideo)(
            repDta, str(day).zfill(5),
            STYLE, framesPth, vLines=[day, STYLE['xRange'][1]]
        ) for day in range(0, int(STYLE['xRange'][1]))
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
        '-start_number', '0',
        '-r', str(15),
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

inPath
outPath