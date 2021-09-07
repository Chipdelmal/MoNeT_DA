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


if monet.isNotebook():
    (USR, REL, CLS) = ('lab', '265', 15)
else:
    (USR, REL, CLS) = (sys.argv[1], sys.argv[2], int(sys.argv[3]))
STP_ONLY = True
CLUSTER_EXPORT = False
(CLUSTERS, LABELS) = (False, False)
(SITES_STUDY, SITES_SOUTH) = (True, False)
###############################################################################
# Selecting Paths
###############################################################################
# Base Geo Path ---------------------------------------------------------------
PTH_ROT = aux.selectPathGeo(USR)
# Population files ------------------------------------------------------------
# if REL == '265':
PTH_PTS = PTH_ROT #+ 'cluster_1/'
filename = 'stp_cluster_sites_pop_v5_fixed.csv'
kernelName = 'kernel_cluster_v6a.csv'
notAccessible = {51, 239}
# elif REL == '106':
#     PTH_PTS = PTH_ROT + 'cluster_2/'
#     filename = 'stp_cluster_sites_pop_01_v5_fixed.csv'
#     kernelName = 'kernel_cluster_01_v5.csv'
#     notAccessible = {32, 99, 102}
# elif REL == '505':
#     PTH_PTS = PTH_ROT + 'regular/'
#     filename = 'stp_all_sites_pop_v5_fixed.csv'
#     kernelName = 'kernel_1_1029.csv'
#     notAccessible = {81, 360, 400, 405, 419}
###############################################################################
# ID clusters
###############################################################################
pts = pd.read_csv(PTH_PTS+filename)
df = pts[['lon', 'lat']]
kmeans = KMeans(n_clusters=CLS, random_state=7415341).fit(df)
df['clst'] = kmeans.labels_
ids = [i for i in range(df.shape[0])]
df['id'] = ids
# Blacklist -------------------------------------------------------------------
(clstLst, clstNum) = (list(df['clst']), len(set(kmeans.labels_)))
count = 0
for (i, nid) in enumerate(clstLst):
    if i in notAccessible:
        clstLst[i] = count+clstNum
        count = count + 1
df['clst'] = clstLst
###############################################################################
# Read Network
###############################################################################
xy = np.genfromtxt(path.join(PTH_ROT, 'mov/001_STP_XY.csv'), delimiter=',')
psi = np.genfromtxt(path.join(PTH_ROT, 'mov/001_STP_MX.csv'), delimiter=',')
np.fill_diagonal(psi, 0)
psiN = normalize(psi, axis=1, norm='l2')
###############################################################################
# Export
###############################################################################
df.to_csv(PTH_PTS+'clusters_'+str(CLS).zfill(3)+'.csv')
# sns.scatterplot(data=df, x="lon", y="lat", style="clst")
clstIDs = list(sorted(set(df['clst'])))
centroid = []
groupings = []
for clstID in clstIDs:
    tmpDF = df[df['clst'] == clstID]
    centroid.append([np.mean(i) for i in (tmpDF['lon'], tmpDF['lat'])])
    groupings.append(list(tmpDF['id']))
pkl.dump(groupings, PTH_PTS+'clusters_'+str(CLS).zfill(3), compression='bz2')
# #############################################################################
# Export Map
# #############################################################################
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
# Sites Highlight -------------------------------------------------------------
prep=prepL+'M_CLEAN_'
if SITES_SOUTH:
    relSites = set(aux.SOUTH)
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
    prep=prepL+'M_SOUTH_'
if SITES_STUDY:
    relSites = set(aux.SITES)
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
    prep=prepL+'M_SITES_'
# Labels ----------------------------------------------------------------------
if LABELS:
    for i in range(len(lon)):
        (x, y) = mH(lon[i], lat[i])
        ax.annotate(
            i, xy=(x, y), size=1, 
            ha='center', va='center', color='white',
            zorder=10, fontsize=0.5
        )
plo.plotNetworkOnMap(mL, psiN, xy, xy, c='#04011f55', lw=.1)
fig.savefig(
    PTH_PTS+prep+str(CLS).zfill(3)+'.png', 
    dpi=2000, bbox_inches='tight', pad_inches=0
)
if CLUSTERS:
    mH.scatter(
        [i[0] for i in centroid], [i[1] for i in centroid], latlon=True,
        alpha=.5, marker='2', s=75,
        color='#233090', zorder=11
    )
if LABELS:
    for i in range(len(centroid)):
        (x, y) = mH(centroid[i][0], centroid[i][1])
        ax.annotate(
            i, xy=(x, y), size=2, 
            ha='center', va='center', zorder=12
        )
fig.savefig(
    PTH_PTS + prep + 'comms_'+str(CLS).zfill(3)+'.png', 
    dpi=2000, 
    bbox_inches='tight', pad_inches=0
)
r=.03
CLS_LB = list(df['clst'])
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
    PTH_PTS + prep + 'clusters_'+str(CLS).zfill(3)+'.png', 
    dpi=2000, 
    bbox_inches='tight', pad_inches=0
)
plt.close('all')
# #############################################################################
# Kernel Heatmap
# #############################################################################
# kernel = np.genfromtxt(PTH_PTS + kernelName, delimiter=',')
# np.fill_diagonal(kernel, 0)
# fig = plt.figure(figsize=(5, 5))
# plt.imshow(kernel, interpolation='nearest', cmap='Purples', vmax=2e-04, vmin=0)
# fun.quickSaveFig(PTH_PTS + 'heat.png', fig, dpi=1000)

