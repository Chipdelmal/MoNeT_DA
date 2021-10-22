
import math
import numpy as np
from os import path
import pandas as pd
import numpy.random as rand
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
import TRP_aux as aux


if monet.isNotebook():
    (POINTS, EXP_FNAME) = (100, '000')
    (PT_DTA, PT_IMG) = aux.selectPaths('dsk')
else:
    POINTS = argv[1]
    (PT_DTA, PT_IMG) = aux.selectPaths(argv[2])
###############################################################################
# Constants
###############################################################################
(xRan, yRan) = ((-10, 10), (-10, 10))
PTS_TMAT = np.asarray([
    [0, 1, 0],
    [.05, 0, .95], 
    [.95, 0, 0.05]
])
PTYPE_PROB = [.1, .7, .2]
###############################################################################
# Generate pointset
###############################################################################
coords = list(zip(rand.uniform(*xRan, POINTS), rand.uniform(*yRan, POINTS)))
# pTypes = rand.randint(0, PTS_TMAT.shape[0], POINTS)
pTypes = np.array(PTYPE_PROB).cumsum().searchsorted(np.random.sample(POINTS))
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
###############################################################################
# Check matrices
###############################################################################
(fig, ax) = plt.subplots(1, 3, figsize=(15, 15))
ax[0].matshow(tau, vmax=.05, cmap=plt.cm.Purples_r)
ax[1].matshow(msk, cmap=plt.cm.Blues)
ax[2].matshow(tauN, vmax=.05, cmap=plt.cm.Purples_r)
fig.savefig(
    path.join(PT_IMG, '{}-{}_Mat.png'.format(EXP_FNAME, str(POINTS).zfill(3))), 
    dpi=250, bbox_inches='tight', pad_inches=0
)
plt.close('all')
###############################################################################
# Plot Landscape
###############################################################################
(LW, ALPHA, SCA) = (.125, .5, 50)
mrkrs = aux.MKRS
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
fig.savefig(
    path.join(PT_IMG, '{}-{}.png'.format(EXP_FNAME, str(POINTS).zfill(3))), 
    dpi=250, bbox_inches='tight', pad_inches=0
)
plt.close('all')
###############################################################################
# Export files
###############################################################################
np.savetxt(
    path.join(PT_DTA, '{}-{}_MX.csv'.format(EXP_FNAME, str(POINTS).zfill(3))), 
    tauN, delimiter=','
)
df = pd.DataFrame(sites, columns=['X', 'Y'])
df['type'] = pTypes
df.to_csv(
    path.join(PT_DTA, '{}-{}_XY.csv'.format(EXP_FNAME, str(POINTS).zfill(3))),
    index=False, header=False
)