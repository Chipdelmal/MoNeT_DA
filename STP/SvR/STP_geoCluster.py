#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import STP_functions as fun
import STP_plots as plo
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import compress_pickle as pkl
import STP_aux as aux


(USR, REL) = ('dsk', '265')
clusters = 2

###############################################################################
# Selecting Paths
###############################################################################
if USR == 'srv':
    PTH_ROT = '/RAID5/marshallShare/STP/SPA/GEO/'
else:
    PTH_ROT = '/home/chipdelmal/Documents/WorkSims/STP/SPA/GEO/'
if REL == '265':
    PTH_PTS = PTH_ROT + 'cluster_1/'
    filename = 'stp_cluster_sites_v5.csv'
###############################################################################
# ID clusters
###############################################################################
pts = pd.read_csv(PTH_PTS+filename)
df = pts[['lon', 'lat']]
kmeans = KMeans(n_clusters=clusters, random_state=7415341).fit(df)
df['clst'] = kmeans.labels_
ids = [i for i in range(df.shape[0])]
df['id'] = ids
###############################################################################
# Export
###############################################################################
df.to_csv(PTH_PTS+'clusters.csv')
# sns.scatterplot(data=df, x="lon", y="lat", style="clst")
clstIDs = list(sorted(set(kmeans.labels_)))
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
mH.scatter(
    list(pts['lon']), list(pts['lat']), latlon=True,
    alpha=.1, marker='.', s=[1],
    color='#E048B8', zorder=3
)
mH.scatter(
    [i[0] for i in centroid], [i[1] for i in centroid], latlon=True,
    alpha=.5, marker='x', s=[5],
    color='#233090', zorder=3
)
fun.quickSaveFig(PTH_PTS + 'clusters.png', fig, dpi=750)
