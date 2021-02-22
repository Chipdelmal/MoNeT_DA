#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import compress_pickle as pkl
import STP_aux as aux
import STP_plots as plo
import STP_functions as fun


if monet.isNotebook():
    (USR, REL, CLS) = ('dsk', '505', 30)
else:
    (USR, REL, CLS) = (sys.argv[1], sys.argv[2], int(sys.argv[3]))
###############################################################################
# Selecting Paths
###############################################################################
# Base Geo Path ---------------------------------------------------------------
if USR == 'srv':
    PTH_ROT = '/RAID5/marshallShare/STP/SPA/GEO/'
else:
    PTH_ROT = '/home/chipdelmal/Documents/WorkSims/STP/SPA/GEO/'
# Population files ------------------------------------------------------------
if REL == '265':
    PTH_PTS = PTH_ROT + 'cluster_1/'
    filename = 'stp_cluster_sites_pop_v5_fixed.csv'
    kernelName = 'kernel_cluster_v5.csv'
    notAccessible = {51, 216, 239, 241, 244}
elif REL == '106':
    PTH_PTS = PTH_ROT + 'cluster_2/'
    filename = 'stp_cluster_sites_pop_01_v5_fixed.csv'
    kernelName = 'kernel_cluster_01_v5.csv'
    notAccessible = {32, 99, 102}
elif REL == '505':
    PTH_PTS = PTH_ROT + 'regular/'
    filename = 'stp_all_sites_pop_v5_fixed.csv'
    kernelName = 'kernel_1_1029.csv'
    notAccessible = {81, 360, 400, 405, 419}
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
# Export
###############################################################################
# df.to_csv(PTH_PTS+'clusters.csv')
# sns.scatterplot(data=df, x="lon", y="lat", style="clst")
clstIDs = list(sorted(set(df['clst'])))
centroid = []
groupings = []
for clstID in clstIDs:
    tmpDF = df[df['clst'] == clstID]
    centroid.append([np.mean(i) for i in (tmpDF['lon'], tmpDF['lat'])])
    groupings.append(list(tmpDF['id']))
pkl.dump(groupings, PTH_PTS + 'clusters', compression='bz2')
# #############################################################################
# Export Map
# #############################################################################
COLORS = plo.COLORS
(minLat, minLong) = (-0.045, 6.4)
(maxLat, maxLong) = (1.75, 7.5)
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
mH = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='h', ax=ax
)
mH.drawcoastlines(color=COLORS[0], linewidth=2, zorder=1)
mH.drawcoastlines(color=COLORS[3], linewidth=.25, zorder=2)
mL = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='i', ax=ax
)
mL.drawcoastlines(color=COLORS[4], linewidth=10, zorder=0)
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
    alpha=.25, marker='.', s=[2],
    color='#E048B8', zorder=3
)
for i in range(len(lon)):
    (x, y) = mH(lon[i], lat[i])
    ax.annotate(i, xy=(x, y), size=.2, ha='center', va='center', color='white')
fun.quickSaveFig(PTH_PTS + 'raw.png', fig, dpi=1000)
mH.scatter(
    [i[0] for i in centroid], [i[1] for i in centroid], latlon=True,
    alpha=.5, marker='x', s=[5],
    color='#233090', zorder=3
)
for i in range(len(centroid)):
    (x, y) = mH(centroid[i][0], centroid[i][1])
    ax.annotate(i, xy=(x, y), size=2, ha='center', va='center')
fun.quickSaveFig(PTH_PTS + 'clusters.png', fig, dpi=1000)
# #############################################################################
# Kernel Heatmap
# #############################################################################
kernel = np.genfromtxt(PTH_PTS + kernelName, delimiter=',')
np.fill_diagonal(kernel, 0)
fig = plt.figure(figsize=(5, 5))
plt.imshow(kernel, interpolation='nearest', cmap='Purples', vmax=2e-04, vmin=0)
fun.quickSaveFig(PTH_PTS + 'heat.png', fig, dpi=1000)
