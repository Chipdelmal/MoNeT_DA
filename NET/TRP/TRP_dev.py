
import numpy as np
from os import path
import networkx as nx
import cdlib.algorithms as cd
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
import TRP_aux as aux

TRAPS_NUM = 10
(PT_DTA, EXP_FNAME) = ('/Volumes/marshallShare/Mov/dta', '00X')
###############################################################################
# Read migration matrix and pop sites
############################################################################### 
pth = path.join(PT_DTA, EXP_FNAME)
migMat = np.genfromtxt(pth+'_MX.csv', delimiter=',')
sites = np.genfromtxt(pth+'_XY.csv', delimiter=',')
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
trapProbs = np.asarray([
    [aux.trapProbability(i, b=0.1) for i in dist] 
    for dist in trapDists
])