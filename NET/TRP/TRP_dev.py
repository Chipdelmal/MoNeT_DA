
import math
import numpy as np
from os import path
import networkx as nx
# import cdlib.algorithms as cd
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
import TRP_aux as aux
import TRP_fun as fun

TRAPS_NUM = 20
(PT_DTA, PT_IMG, EXP_FNAME) = (
    '/Volumes/marshallShare/Mov/dta',
    '/Volumes/marshallShare/Mov/trp',
    '001'
)
kPars = {
    'Trap': {'A': 0.1, 'b': 0.75},
    'Escape': {'A': 0, 'b': 100}
}
###############################################################################
# Read migration matrix and pop sites
############################################################################### 
pth = path.join(PT_DTA, EXP_FNAME)
migMat = np.genfromtxt(pth+'_MX.csv', delimiter=',')
sites = np.genfromtxt(pth+'_XY.csv', delimiter=',')
sitesNum = sites.shape[0]
###############################################################################
# Transitions Matrix and Base Netowrk
###############################################################################
psiN = fun.deleteLoopsFromMatrix(migMat)
# np.apply_along_axis(sum, 1, psiN)
###############################################################################
# Generate some trap locations and calculate distances
###############################################################################
(minX, minY) = np.apply_along_axis(min, 0, sites)
(maxX, maxY) = np.apply_along_axis(max, 0, sites)
traps = fun.placeTrapsRanUnif(TRAPS_NUM, (minX, maxX), (minY, maxY))
trapDists = fun.calcTrapToSitesDistance(traps, sites)
###############################################################################
# Calculate trapping probabilities and assemble matrix
###############################################################################
tProbs = fun.calcTrapsSections(trapDists, params=kPars)
tauN = fun.assembleTrapMigration(psiN, tProbs)
np.apply_along_axis(sum, 1, tauN)
# np.apply_along_axis(sum, 1, F)
###############################################################################
# Plot matrix
###############################################################################
(fig, ax) = plt.subplots(figsize=(15, 15))
plt.imshow(tauN, vmax=1e-1, cmap='Purples', interpolation='nearest')
fig.savefig(
    path.join(PT_IMG, EXP_FNAME+'_trapsMatrix.png'), 
    dpi=500, bbox_inches='tight'
)
###############################################################################
# Plot landscape
###############################################################################
BBN = tauN[:sitesNum, :sitesNum]
BQN = tauN[:sitesNum, sitesNum:]
(LW, ALPHA, SCA) = (.125, .2, 50)
(fig, ax) = plt.subplots(figsize=(15, 15))
(fig, ax) = aux.plotNetwork(fig, ax, BQN*SCA, traps, sites, [0], c='#f72585', lw=LW, alpha=ALPHA)
(fig, ax) = aux.plotNetwork(fig, ax, BBN*SCA, sites, sites, [0], c='#2B62F7', lw=LW, alpha=ALPHA)
plt.scatter(sites.T[0], sites.T[1], marker='^', color='#ef233cDB', s=50, zorder=10)
plt.scatter(traps.T[0], traps.T[1], marker='o', color='#03045eDB', s=50, zorder=10)
plt.tick_params(
    axis='both', which='both',
    bottom=False, top=False, left=False, right=False,
    labelbottom=False, labeltop=False, labelleft=False, labelright=False
) # labels along the bottom edge are off
fig.savefig(
    path.join(PT_IMG, EXP_FNAME+'_trapsNetwork.png'), 
    dpi=250, bbox_inches='tight'
)

###############################################################################
# Calculate metrics
###############################################################################
# Re-arrange matrix in canonical form -----------------------------------------
canO = list(range(sitesNum, sitesNum+TRAPS_NUM))+list(range(0, sitesNum))
tauCan = np.asarray([[tauN[i][j] for j in canO] for i in canO])
# plt.imshow(tauCan, vmax=1e-1, cmap='Purples', interpolation='nearest')
A = tauCan[TRAPS_NUM:, :TRAPS_NUM]
B = tauCan[TRAPS_NUM:, TRAPS_NUM:]
F = np.linalg.inv(np.subtract(np.identity(B.shape[0]), B))
daysTillTrapped = np.apply_along_axis(sum, 1, F)
sum(daysTillTrapped)

###############################################################################
# Verify metrics
###############################################################################
# tst = np.linalg.matrix_power(tauN, 1000000000)
# # plt.imshow(tst[:sitesNum, -TRAPS_NUM:].T, cmap='Purples', interpolation='nearest')
# catchesA = tst[:sitesNum, -TRAPS_NUM:]
# catchesB = np.matmul(F, A)
# plt.imshow(F, cmap='Purples', interpolation='nearest')

###############################################################################
# Debug math
###############################################################################
# tst = np.asarray(
#     [
#         [0, .5, 0, .5, 0],
#         [.5, 0, .5, 0, 0],
#         [0, .5, 0, 0, .5],
#         [0, 0, 0, 1, 0],
#         [0, 0, 0, 0, 1]
#     ]
# )
# tst = np.asarray(
#     [
#         [0, .5, 0],
#         [.5, 0, .5],
#         [0, .5, 0]
#     ]
# )
# n = np.linalg.inv(np.subtract(np.identity(3), tst))
# r = np.asarray(
#     [
#         [.5, 0],
#         [0, 0],
#         [0, .5]
#     ]
# )
# np.matmul(n, r)


psiN = np.asarray(
    [
        [0, .5, 0],
        [.5, 0, .5],
        [0, .5, 0]
    ]
)
trap = np.asarray([
    [.5, 0],
    [0, 0],
    [0, .5]
])
N = np.linalg.inv(np.subtract(np.identity(psiN.shape[0]), psiN))
np.matmul(N, trap)

tauN[:sitesNum, -TRAPS_NUM:]