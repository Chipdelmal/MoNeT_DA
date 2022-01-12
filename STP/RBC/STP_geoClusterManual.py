#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
from os import path
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import compress_pickle as pkl
from descartes import PolygonPatch
import shapely
import STP_aux as aux
import STP_auxDebug as plo


(USR, REL, STH_SITE) = ('dsk', '265', True)
(SITES_STUDY, SITES_SOUTH) = (True, False)
SPLIT_IX = 27
###############################################################################
if STH_SITE:
    relSite = aux.SOUTH
else:
    relSite = aux.SITES
###############################################################################
# Paths
###############################################################################
PTH_ROT = aux.selectPathGeo(USR)
PTH_PTS = PTH_ROT #+ 'cluster_1/'
filename = 'stp_cluster_sites_pop_v5_fixed.csv'
kernelName = 'kernel_cluster_v6a.csv'
notAccessible = {51, 239}
###############################################################################
# ID clusters
###############################################################################
pts = pd.read_csv(PTH_PTS+filename)
df = pts[['lon', 'lat']]
kmeans = KMeans(n_clusters=CLS, random_state=7415341).fit(df)
df['clst'] = kmeans.labels_
ids = [i for i in range(df.shape[0])]
df['id'] = ids
SAO_TOME_LL = df.iloc[SPLIT_IX:]
PRINCIPE_LL = df.iloc[:SPLIT_IX]
###############################################################################
# Read Network
###############################################################################
xy = np.genfromtxt(path.join(PTH_ROT, 'mov/001_STP_XY.csv'), delimiter=',')
psi = np.genfromtxt(path.join(PTH_ROT, 'mov/001_STP_MX.csv'), delimiter=',')
np.fill_diagonal(psi, 0)
psiN = normalize(psi, axis=1, norm='l2')
###############################################################################
# Un-aggregated
###############################################################################
notAggregate = set(relSite)
aggregate = set(df['id'])-notAggregate-set(PRINCIPE_LL['id'])-notAccessible
###############################################################################
# Un-aggregated
###############################################################################
lnd = df.copy()
# Principe --------------------------------------------------------------------
currIx = 0
lnd['clst'].iloc[:SPLIT_IX] = currIx
# Sao Tome (No Release) -------------------------------------------------------
currIx = currIx + 1
for i in list(aggregate):
    lnd['clst'].iloc[i] = currIx
# Sao Tome (Release) ----------------------------------------------------------
currIx = currIx + 1
for i in list(notAggregate):
    lnd['clst'].iloc[i] = currIx
    currIx = currIx + 1
# Inaccesible -----------------------------------------------------------------
for i in list(notAccessible):
    lnd['clst'].iloc[i] = currIx
    currIx = currIx + 1
###############################################################################
# Checking Aggregation
###############################################################################
clusters = list(lnd['clst'])
aggrMat = monet.aggregateLandscape(psiN, clusters)

set(lnd['clst'])

len(notAggregate)
len(aggregate)
len(notAccessible)