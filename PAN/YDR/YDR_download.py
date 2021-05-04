
import sys
import subprocess
from os import path
import YDR_gene as drv
import MoNeT_MGDrivE as monet

if monet.isNotebook():
    (SET, DRV, SUB, IMG) = ('shredder', 'AXS', 'preGrids', True)
else:
    (SET, DRV, SUB, IMG) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
EXPS = ('001', )
# EXPS = ('000', '002', '004', '006', '008')
###############################################################################
# Paths
###############################################################################
(LAB_BASE, DSK_BASE) = (
    'lab:/RAID5/marshallShare/yLinked2/',
    '/home/chipdelmal/Documents/WorkSims/YDR/'
)
# Create structure in local computer ------------------------------------------
geneFldr = drv.driveSelector(DRV, 'ECO').get('folder')
(PT_SET_S, PT_SET_T) = [path.join(i, SET) for i in (LAB_BASE, DSK_BASE)]
(PT_DRV_S, PT_DRV_T) = [path.join(i, geneFldr) for i in (PT_SET_S, PT_SET_T)]
[monet.makeFolder(i) for i in (PT_SET_T, PT_DRV_T)]
###############################################################################
# Paths
###############################################################################
CPY_STR = 'scp -r {} {}'
(i, exp) = (0, EXPS[0])
for (i, exp) in enumerate(EXPS):
    if IMG=="True":
        (PT_WRK_S, PT_WRK_T) = [
            path.join(i, exp, 'img') for i in (PT_DRV_S, PT_DRV_T)
        ]        
        (PT_S, PT_T) = [path.join(i, SUB) for i in (PT_WRK_S, PT_WRK_T)]
        PT_T = path.split(PT_T)[0]
    else:
        (PT_WRK_S, PT_WRK_T) = [path.join(i, exp) for i in (PT_DRV_S, PT_DRV_T)]
        (PT_S, PT_T) = [path.join(i, SUB) for i in (PT_WRK_S, PT_WRK_T)]
        PT_T = path.split(PT_T)[0]
    [monet.makeFolder(i) for i in (PT_WRK_T, PT_T)]
    cmd = CPY_STR.format(PT_S , PT_T)
    print('* Downloading {} part {}/{}... '.format(DRV, i+1, len(EXPS)))
    print('\t'+cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()