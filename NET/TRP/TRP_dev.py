
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
import random

random.seed(10)

TRAPS_NUM = 10
(PT_DTA, EXP_FNAME) = ('/Volumes/marshallShare/Mov/dta', '00X')
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
# Delete self-transitions -----------------------------------------------------
np.fill_diagonal(migMat, 0)
psiN = normalize(migMat, axis=1, norm='l2')
# Generate initial migration network ------------------------------------------
G = nx.from_numpy_matrix(psiN)
G.remove_edges_from(nx.selfloop_edges(G))
###############################################################################
# Generate some trap locations
###############################################################################
(minX, minY) = np.apply_along_axis(min, 0, sites)
(maxX, maxY) = np.apply_along_axis(max, 0, sites)
# Locate traps random-uniformly across the landscape --------------------------
traps = np.asarray([
    [
        np.random.uniform(minX, maxX, 1)[0], 
        np.random.uniform(minY, maxY, 1)[0]
    ] for i in range(TRAPS_NUM)
])
###############################################################################
# Calculate trapping probabilities
###############################################################################
trapDists = np.asarray([
    [np.linalg.norm(site-trap) for site in sites]
    for trap in traps
]).T
# Traps attractiveness --------------------------------------------------------
trapProbs = np.asarray([
    [aux.trapProbability(i, b=0.1) for i in dist] 
    for dist in trapDists
])
# Traps identity --------------------------------------------------------------
trapIdentity = np.identity(TRAPS_NUM)
# Traps escape ----------------------------------------------------------------
trapEscape = np.asarray([
    [aux.trapProbability(i, b=10) for i in dist] 
    for dist in trapDists
]).T
###############################################################################
# Assemble matrix
###############################################################################
(n, m) = (sitesNum, TRAPS_NUM)
tau = np.empty((n+m, n+m))
# BB Section --------------------------------------------------------------
BB = psiN
for i in range(n):
    for j in range(n):
        tau[i, j] = BB[i, j]
# BQ Section --------------------------------------------------------------
BQ = trapProbs.T
for i in range(n):
    for j in range(m):
        tau[i, j + n] = BQ[j, i]
# QB Section --------------------------------------------------------------
QB = trapEscape.T
for i in range(n):
    for j in range(m):
        tau[j+n, i] = QB[i, j]
# QQ Section --------------------------------------------------------------
QQ = trapIdentity
for i in range(m):
    for j in range(m):
        tau[i+n, j+n] = QQ[i, j]
###############################################################################
# Normalize and plot matrix
###############################################################################
tauN = normalize(tau, axis=1, norm='l2')
# plt.imshow(tau, vmax=1e-2, interpolation='nearest')
(fig, ax) = plt.subplots(figsize=(15, 15))
# ax.imshow(tauN, vmax=1e-2, cmap='Purples', interpolation='nearest')
# fig.savefig('./out.png', dpi=500)
(fig, ax) = aux.plotNetwork(fig, ax, tauN, traps, sites, [0], c='#2B62F7')
(fig, ax) = aux.plotNetwork(fig, ax, tauN, sites, sites, [0], c='#FB3264')
plt.scatter(sites.T[0], sites.T[1], marker='^')
plt.scatter(traps.T[0], traps.T[1], marker='o')