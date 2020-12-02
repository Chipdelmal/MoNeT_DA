
import sys
import subprocess
from os import path
import YDR_gene as drv
import MoNeT_MGDrivE as monet


(USR, SET, DRV, SUB) = ('dsk', 'homing', 'ASD', 'img')
# (USR, SET, DRV, SUB) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
EXPS = ('000', '002', '004', '006', '008')
###############################################################################
# Paths
###############################################################################
(LAB_BASE, DSK_BASE) = (
    'lab:/RAID5/marshallShare/yLinked/',
    '/home/chipdelmal/Documents/WorkSims/YDR/'
)
base = LAB_BASE
if USR == 'dsk':
    base = DSK_BASE
# Create structure in local computer ------------------------------------------
geneFldr = drv.driveSelector(DRV, 'ECO').get('folder')
PT_DRV = path.join(base, SET, geneFldr)
###############################################################################
# Paths
###############################################################################
DLT_STR = 'rm -r {}'
for (i, exp) in enumerate(EXPS):
    PT_DEL = path.join(PT_DRV , exp, SUB)
    cmd = DLT_STR.format(PT_DEL)
    print('* Downloading {} part {}/{}... '.format(DRV, i+1, len(EXPS)))
    print('\t'+cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()