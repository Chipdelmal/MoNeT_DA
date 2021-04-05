
import sys
import subprocess
from datetime import datetime
import MoNeT_MGDrivE as monet

###############################################################################
# Define inputs
###############################################################################
if monet.isNotebook():
    (USR, DRV, AOI, LND) = ('dsk', 'PGS', 'HLT', 'SPA')
    EXP = 'E_016_024_050_050_050'
else:
    (USR, DRV, AOI, LND, EXP) = (
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    )
id = "{}-{}".format(EXP, AOI)
rate = 15
###############################################################################
# User select
###############################################################################
if USR == 'srv':
    basePath = '/RAID5/marshallShare/pyf/{}/video/'.format(LND)
else:
    basePath = '/home/chipdelmal/Documents/WorkSims/PYF/Onetahi/sims/{}/video/'.format(LND)
###############################################################################
# Define paths
###############################################################################
outName = id
outPath = basePath + outName + '.mp4'
inPath = basePath + id + "/" + '%04d.png'
tS = datetime.now()
monet.printExperimentHead(basePath, outPath, tS, 'PYF PstTraces '+AOI)
###############################################################################
# Launch process
###############################################################################
sp = subprocess.Popen([
    'ffmpeg', '-y', 
    '-loglevel', 'quiet',
    '-start_number', '1',
    '-r', str(rate),
    '-f', 'image2',
    '-s', '1920x1080',
    '-i', inPath,
    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
    '-vcodec', 'libx264',
    '-preset', 'veryslow',
    '-crf', '15',
    '-report',
    '-pix_fmt', 'yuv420p',
    outPath
])
sp.wait()
print("I: " + inPath +"\n" + "O: " + outPath)
