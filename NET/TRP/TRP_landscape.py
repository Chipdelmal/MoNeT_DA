
import math
import numpy as np
import numpy.random as rand
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

POINTS = 50
(xRan, yRan) = ((-10, 10), (-10, 10))
PTS_TMAT = np.asarray([
    [.1, .85, .05],
    [.8, .2, 0],
    [1, 0, 0]
])
# PTS_TMAT = np.asarray([[1]])
###############################################################################
# Generate pointset
###############################################################################
coords = list(zip(
    rand.uniform(*xRan, POINTS), 
    rand.uniform(*yRan, POINTS)
))
pTypes = rand.randint(0, PTS_TMAT.shape[0], POINTS)
###############################################################################
# Generate matrices
###############################################################################
dist = monet.calculateDistanceMatrix(coords)
tau = monet.zeroInflatedExponentialMigrationKernel(
    dist, 
    [0.2, 1.0e-10, math.inf],
    zeroInflation=0.75
)
###############################################################################
# Generate masking matrix
###############################################################################
itr = list(range(len(coords)))
msk = np.zeros((POINTS, POINTS))
r = 0
for r in itr:
    for c in itr:
        msk[r, c] = PTS_TMAT[pTypes[r], pTypes[c]]
tauN = normalize(msk*tau, axis=1, norm='l1')
# np.apply_along_axis(sum, 1, tauN)
###############################################################################
# Check matrices
###############################################################################
plt.matshow(tau, vmax=.05)
plt.matshow(msk)
plt.matshow(tauN, vmax=.05)