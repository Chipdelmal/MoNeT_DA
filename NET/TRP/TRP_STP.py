
import math
import numpy as np
from os import path
from sys import argv
import networkx as nx
# import cdlib.algorithms as cd
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
import TRP_aux as aux
import TRP_fun as fun

TRAPS_NUM = 1
STEP = .25
(PT_DTA, PT_IMG, EXP_FNAME) = (
    '/Volumes/marshallShare/Mov/dta',
    '/Volumes/marshallShare/Mov/trp/Benchmark',
    '003_STP'
)
(dbg, randTrap) = (True, True)
(USR, DRV) = ('dsk', 'SDR')
###############################################################################
# Read migration matrix and pop sites
############################################################################### 
pth = path.join(PT_DTA, EXP_FNAME)
migMat = np.genfromtxt(pth+'_MX.csv', delimiter=',')
sites = np.genfromtxt(pth+'_XY.csv', delimiter=',')
###############################################################################
# Read migration matrix and pop sites
############################################################################### 
migs = migMat[52:, 52:]
sits = sites[52:]
tauN = normalize(migs, axis=1, norm='l1')
###############################################################################
# Read migration matrix and pop sites
############################################################################### 
np.savetxt(path.join(PT_DTA, '004_STP_MX.csv'), tauN, delimiter=",")
np.savetxt(path.join(PT_DTA, '004_STP_XY.csv'), sits, delimiter=",")