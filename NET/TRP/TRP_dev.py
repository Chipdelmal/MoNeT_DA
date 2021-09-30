
import numpy as np
from os import path
import networkx as nx
# import cdlib.algorithms as cd
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering


(PT_DTA, EXP_FNAME) = (
    'PATH_TO_DATA', 
    'EXP_FILENAME'
)
###############################################################################
# Read migration matrix
############################################################################### 
migMat = np.genfromtxt(
    path.join(PT_DTA, EXP+'_MX.csv'), 
    delimiter=','
)
sites = np.genfromtxt(
    path.join(PT_DTA, EXP+'_XY.csv'), 
    delimiter=','
)
###############################################################################
# Transitions Matrix and Base Netowrk
###############################################################################
# Delete self-transitions -----------------------------------------------------
np.fill_diagonal(migMat, 0)
psi = normalize(migMat, axis=1, norm='l2')
# Generate initial migration network ------------------------------------------
G = nx.from_numpy_matrix(psiN)
G.remove_edges_from(nx.selfloop_edges(G))