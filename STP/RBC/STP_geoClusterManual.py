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


(USR, REL, STH_SITE) = ('dsk', '265', False)
(SITES_STUDY, SITES_SOUTH) = (True, False)
STP_ONLY = True
SPLIT_IX = 27
###############################################################################
if STH_SITE:
    (rid, relSite) = ('SOUTH', aux.SOUTH)
else:
    (rid, relSite) = ('SITES', aux.SITES)
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
psiN = normalize(psi, axis=1, norm='l1')
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
aggMat = monet.aggregateLandscape(psiN, clusters)
###############################################################################
# Export
###############################################################################
lnd.to_csv(PTH_ROT+rid+'_v2_coords.csv', index=False)
np.savetxt(PTH_ROT+rid+'_v2_migmat.csv', aggMat, delimiter=",")
###############################################################################
# Export Map
###############################################################################
clstIDs = list(sorted(set(lnd['clst'])))
centroid = []
groupings = []
for clstID in clstIDs:
    tmpDF = lnd[lnd['clst'] == clstID]
    centroid.append([np.mean(i) for i in (tmpDF['lon'], tmpDF['lat'])])
    groupings.append(list(tmpDF['id']))

COLORS = plo.COLORS
(minLat, minLong) = (-0.045, 6.4)
(maxLat, maxLong) = (1.75, 7.5)
prepL=''
if STP_ONLY:
    (minLat, minLong) = (-0.045, 6.4)
    (maxLat, maxLong) = (.5, 6.85)
    prepL='STP_'
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
mH = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='h', ax=ax
)
mH.drawcoastlines(color=COLORS[0], linewidth=3, zorder=-3)
mH.drawcoastlines(color=COLORS[3], linewidth=.5, zorder=-2)
mL = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='i', ax=ax
)
mL.drawcoastlines(color=COLORS[4], linewidth=6, zorder=-1)
ax.tick_params(
    axis='both', which='both',
    bottom=True, top=False, left=True, right=False,
    labelbottom=True, labelleft=True
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
(lon, lat) = (list(pts['lon']), list(pts['lat']))
mH.scatter(
    lon, lat, latlon=True,
    alpha=.8, marker='o', s=[math.log(1+i/10)/.2 for i in pts['pop']],
    color='#ff006e', zorder=10, 
    edgecolors='#ffffff', linewidth=.5
)
# mH.scatter(
#     [i[0] for i in centroid], [i[1] for i in centroid], latlon=True,
#     alpha=.5, marker='2', s=75,
#     color='#233090', zorder=11
# )
prep=prepL+'M_CLEAN_'
if STH_SITE:
    relSites = relSite
    (lonR, latR, popR) = [
        [l for (i, l) in enumerate(lon) if (i) in relSites],
        [l for (i, l) in enumerate(lat) if (i) in relSites],
        [l for (i, l) in enumerate(pts['pop']) if (i) in relSites]
    ]
    mH.scatter(
        lonR, latR, latlon=True,
        alpha=.8, marker='o', s=[math.log(1+i/10)/.2 for i in popR],
        color='#03045e', zorder=10, 
        edgecolors='#ffffff', linewidth=.5
    )
else:
    relSites = relSite
    (lonR, latR, popR) = [
        [l for (i, l) in enumerate(lon) if (i) in relSites],
        [l for (i, l) in enumerate(lat) if (i) in relSites],
        [l for (i, l) in enumerate(pts['pop']) if (i) in relSites]
    ]
    mH.scatter(
        lonR, latR, latlon=True,
        alpha=.8, marker='o', s=[math.log(1+i/10)/.2 for i in popR],
        color='#03045e', zorder=10, 
        edgecolors='#ffffff', linewidth=.5
    )
r=.025
CLS_LB = list(lnd['clst'])
X = xy
D = plo.disjoint_polygons(X, radius=r, n_angles=50)
for j in list(set(CLS_LB)):
    matches = [key for key, val in enumerate(CLS_LB) if val in set([j])]
    base = D.geometry[matches[0]]
    for i in range(len(matches)):
        base = base.union(D.geometry[matches[i]].buffer(.01*r))
        mpoly = shapely.ops.transform(mH, base)
    ax.add_patch(
        PolygonPatch(
            mpoly, fc="none", ec='#6347ff', lw=1.25, alpha=.2, zorder=1
        )
    )
    ax.add_patch(
        PolygonPatch(
            mpoly, fc="none", ec='#ffffff', lw=.35, alpha=1, zorder=2
        )
    )
fig.savefig(
    PTH_ROT+rid+'_v2_MAP.png', 
    dpi=500, 
    bbox_inches='tight', pad_inches=0
)