
import sys
from os import path
import subprocess
import STP_aux as aux
import MoNeT_MGDrivE as monet


if monet.isNotebook():
    (USR, AOI, LND, DRV, exp) = ('lab', 'HLT', 'SPA', 'LDR', '265_SS')
    EXP = 'E_01_12_00500_000790000000_000100000000_0017500_0011700_0000000_0100000_0095600'
else:
    (USR, AOI, LND, DRV, exp) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    EXP = sys.argv[6]
rate = 30
###############################################################################
# User select
###############################################################################
idName = "{}-{}".format(EXP, AOI)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, exp, LND, DRV
)
PT_VID = path.join(PT_IMG, 'preVideo')
###############################################################################
# Define paths
###############################################################################
outName = idName
outPath = PT_VID + '/' + outName + '.mp4'
inPath = PT_VID + '/' + idName + '/' + '%04d.png'
###############################################################################
# Launch process
###############################################################################
sp = subprocess.Popen([
    'ffmpeg',
    # '-loglevel', '+info',
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
