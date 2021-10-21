
import math
import numpy as np
import numpy.random as rand
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
import TRP_aux as aux

POINTS = 25
(xRan, yRan) = ((-10, 10), (-10, 10))
PTS_TMAT = np.asarray([
    [0.05, 0.95],
    [0.20, 0.80]
])
# PTS_TMAT = np.asarray([[1]])
###############################################################################
# Generate pointset
###############################################################################
coords = list(zip(rand.uniform(*xRan, POINTS), rand.uniform(*yRan, POINTS)))
pTypes = rand.randint(0, PTS_TMAT.shape[0], POINTS)
sites = np.asarray(coords)
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
###############################################################################
# Plot Landscape
###############################################################################
(LW, ALPHA, SCA) = (.125, .5, 50)
mrkrs = ('X', 'o', "^")
(fig, ax) = plt.subplots(figsize=(15, 15))
for (i, site) in enumerate(sites):
    plt.scatter(
        site[0], site[1], 
        marker=mrkrs[pTypes[i]], color='#03045eDB', 
        s=250, zorder=20, edgecolors='w', linewidths=2
    )
ax.set_xlim(*xRan)
ax.set_ylim(*yRan)
(fig, ax) = aux.plotNetwork(
    fig, ax, tauN*SCA, sites, sites, [1]*len(coords), 
    c='#03045e', lw=LW, alpha=ALPHA, arrows=False
)