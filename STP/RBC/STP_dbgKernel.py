
from os import path
import numpy as np


(kernelPath, kernelName) = (
    '/home/chipdelmal/Documents/WorkSims/STP_Grid/GEO_v2_Debug/',
    'kernel_cluster_v6a.csv'
)
relSites = (
    37, 48, 54, 53, 61, 59, 58, 75, 78, 84, 94, 65, 67, 68,
    104, 111, 131, 102, 93, 96, 90, 115, 116, 132, 123, 129, 
    141, 109, 156, 169,

    50
)
###############################################################################
# Read Kernel and Init New Kernel
###############################################################################
bKrnl = np.genfromtxt(path.join(kernelPath, kernelName), delimiter=',')
sNum = len(relSites)+1
nKrnl = np.zeros((sNum, sNum))
###############################################################################
# Fill new matrix
###############################################################################
(rn, cn) = (0, 0)
for row in relSites:
    for col in relSites:
        nKrnl[rn, cn] = bKrnl[row, col]
        cn = cn+1
    (rn, cn) = (rn+1, 0)
###############################################################################
# Export new matrix
###############################################################################
np.savetxt(
    path.join(kernelPath, 'debugKernel.csv'),
    nKrnl, delimiter=','
)