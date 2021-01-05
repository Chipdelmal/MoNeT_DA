
import sys
import subprocess

###############################################################################
# Define inputs
###############################################################################
(USR, AOI, REL, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# (USR, AOI, REL, LND, MGV) = ('dsk', 'HLT', '265', 'SPA', 'v1')
id = "{}-{}".format('E_0020000000_03_0000000100_0100000000_0000015730', 'HLT')
# basePath = "/home/chipdelmal/Documents/WorkSims/STP/SPA/505/video/"
rate = 30
###############################################################################
# User select
###############################################################################
if USR == 'srv':
    basePath = '/RAID5/marshallShare/STP/{}/sim/{}/video/'.format(LND, REL)
else:
    basePath = '/home/chipdelmal/Documents/WorkSims/STP/{}/{}/video/'.format(LND, REL)
###############################################################################
# Define paths
###############################################################################
outName = id
outPath = basePath + outName + '.mp4'
inPath = basePath + id + "/" + '%04d.png'
###############################################################################
# Launch process
###############################################################################
sp = subprocess.Popen([
    'ffmpeg',
    '-loglevel', '+info',
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
