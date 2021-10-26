
import math
import numpy as np
from os import path
import pandas as pd
import numpy.random as rand
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
import TRP_aux as aux


(LND, MOD) = ('UNF', 'HET')
if monet.isNotebook():
    (POINTS, EXP_FNAME) = (200, 'UNIF_MD')
    (PT_DTA, PT_IMG) = aux.selectPaths('lab')
else:
    POINTS = argv[1]
    (PT_DTA, PT_IMG) = aux.selectPaths(argv[2])
###############################################################################
# Constants
###############################################################################
sca = 40
(xRan, yRan) = ((-1280/sca, 1280/sca), (-720/sca, 720/sca))
# (xRan, yRan) = ((-10, 10), (-10, 10))
if MOD == 'HOM':
    PTS_TMAT = np.asarray([
        [1/3, 1/3, 1/3],
        [1/3, 1/3, 1/3], 
        [1/3, 1/3, 1/3]
    ])
else:
    PTS_TMAT = np.asarray([
        [0.05, 0.9, .05],
        [.05, .05, .9], 
        [.9, 0.05, 0.05]
    ])
PTYPE_PROB = [.1, .6, .3]
KERNEL = [2, 1.0e-10, math.inf]
###############################################################################
# Generate pointset
###############################################################################
if LND == 'Grid':
    x = np.linspace(xRan[0], xRan[1], int((xRan[1]-xRan[0])/3))
    y = np.linspace(yRan[0], yRan[1], int((yRan[1]-yRan[0])/3))
    coords = np.asarray(np.meshgrid(x, y)).T
    coords = np.concatenate(coords)
else:
    coords = list(zip(rand.uniform(*xRan, POINTS), rand.uniform(*yRan, POINTS)))
# Point-types -----------------------------------------------------------------
pNum = len(list(coords))
pTypes = np.array(PTYPE_PROB).cumsum().searchsorted(np.random.sample(pNum))
sites = np.asarray(coords)
###############################################################################
# Generate matrices
###############################################################################
dist = monet.calculateDistanceMatrix(coords)
tau = monet.zeroInflatedExponentialMigrationKernel(
    dist, KERNEL, zeroInflation=0.75
)
###############################################################################
# Generate masking matrix
###############################################################################
itr = list(range(len(coords)))
msk = np.zeros((pNum, pNum))
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
    path.join(PT_DTA, '{}-{}-{}_Mat.png'.format(
        EXP_FNAME, str(pNum).zfill(3), MOD
    )), dpi=250, bbox_inches='tight', pad_inches=0
)
plt.close('all')
###############################################################################
# Plot Landscape
###############################################################################
(LW, ALPHA, SCA) = (.125, .5, 50)
tauC = np.clip(tauN, 1e-10, 1)
(fig, ax) = plt.subplots(figsize=(15, 15))
for (i, site) in enumerate(sites):
    plt.scatter(
        site[0], site[1], 
        marker=aux.MKRS[pTypes[i]], 
        color=aux.MCOL[pTypes[i]], 
        s=200, zorder=20, edgecolors='w', linewidths=2
    )
ax.set_xlim(*xRan)
ax.set_ylim(*yRan)
ax.set_aspect('equal')
(fig, ax) = aux.plotNetwork(
    fig, ax, tauC*SCA, sites, sites, [1]*len(coords), 
    c='#03045e', lw=LW, alpha=ALPHA, arrows=False
)
fig.savefig(
    path.join(PT_DTA, '{}-{}-{}.png'.format(
        EXP_FNAME, str(pNum).zfill(3), MOD
    )), dpi=250, bbox_inches='tight', pad_inches=0
)
plt.close('all')
###############################################################################
# Export files
###############################################################################
np.savetxt(
    path.join(PT_DTA, '{}-{}-{}_MX.csv'.format(
        EXP_FNAME, str(pNum).zfill(3), MOD
    )), tauN, delimiter=','
)
df = pd.DataFrame(sites, columns=['X', 'Y'])
df['type'] = pTypes
df.to_csv(
    path.join(PT_DTA, '{}-{}-{}_XY.csv'.format(
        EXP_FNAME, str(pNum).zfill(3), MOD
    )), index=False, header=False
)
plt.close('all')
