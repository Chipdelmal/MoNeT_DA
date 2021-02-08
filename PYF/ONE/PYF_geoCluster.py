#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from sklearn.cluster import KMeans
import compress_pickle as pkl
import PYF_aux as aux
# import PYF_functions as fun
import PYF_plots as plo
import MoNeT_MGDrivE as monet


if monet.isNotebook():
    (USR, CLS) = ('dsk', 15)
else:
    (USR, CLS) = (sys.argv[1], int(sys.argv[2]))
###############################################################################
# Selecting Paths
###############################################################################
# Base Geo Path ---------------------------------------------------------------
if USR == 'srv':
    PTH_ROT = '/RAID5/marshallShare/pyf/GEO/'
else:
    PTH_ROT = '/home/chipdelmal/Documents/WorkSims/PYF/Onetahi/GEO/'
PTH_PTS = PTH_ROT
filename = 'Onetahi.csv'
# kernelName = 'kernel_cluster_v5.csv'
SHPFS = ('bh400kc3500', 'Onetahi')
(COLORS, DPI) = (plo.COLORS, 500)
###############################################################################
# ID clusters
###############################################################################
pts = pd.read_csv(path.join(PTH_PTS, filename))
df = pts[['lons', 'lats']]
kmeans = KMeans(n_clusters=CLS, random_state=7415341).fit(df)
df['clst'] = kmeans.labels_
ids = [i for i in range(df.shape[0])]
df['id'] = ids
###############################################################################
# Export
###############################################################################
# df.to_csv(PTH_PTS+'clusters.csv')
# sns.scatterplot(data=df, x="lon", y="lat", style="clst")
clstIDs = list(sorted(set(kmeans.labels_)))
centroid = []
groupings = []
for clstID in clstIDs:
    tmpDF = df[df['clst'] == clstID]
    centroid.append([np.mean(i) for i in (tmpDF['lons'], tmpDF['lats'])])
    groupings.append(list(tmpDF['id']))
pkl.dump(groupings, PTH_PTS + 'clusters', compression='bz2')
# #############################################################################
# Export Map
# #############################################################################
COLORS = plo.COLORS
PAD = .00675
point = (-17.0187975, -149.591045)
(minLat, minLong) = [i-PAD for i in point]
(maxLat, maxLong) = [i+PAD for i in point]
# Generate map ----------------------------------------------------------------
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
# Geography -------------------------------------------------------------------
mH = Basemap(
    projection='merc', lat_ts=20, resolution='h', ax=ax,
    llcrnrlat=minLat, urcrnrlat=maxLat, llcrnrlon=minLong, urcrnrlon=maxLong   
)
mH.readshapefile(
    PTH_PTS+SHPFS[0], 'PYF', 
    drawbounds=True, linewidth=15, color=COLORS[4], zorder=-1
)
mH.readshapefile(
    PTH_PTS+SHPFS[0], 'PYF', 
    drawbounds=True, linewidth=4, color=COLORS[0], zorder=2
)
mH.readshapefile(
    PTH_PTS+SHPFS[0], 'PYF', 
    drawbounds=True, linewidth=1, color=COLORS[3], zorder=2
)
# Buildings -------------------------------------------------------------------
mH.readshapefile(
    PTH_PTS+SHPFS[1], 'One', 
    drawbounds=True, linewidth=1, color=COLORS[1], zorder=3
)
patches   = []
for info, shape in zip(mH.One_info, mH.One):
    patches.append(Polygon(np.array(shape), True))
ax.add_collection(
    PatchCollection(
        patches, facecolor= COLORS[1], edgecolor=None, linewidths=1., zorder=2
    )
)
# Remove axes -----------------------------------------------------------------
ax.tick_params(
    axis='both', which='both',
    bottom=True, top=False, left=True, right=False,
    labelbottom=True, labelleft=True
)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
# Clusters --------------------------------------------------------------------
(lon, lat) = (list(pts['lons']), list(pts['lats']))
# mH.scatter(
#     lon, lat, latlon=True,
#     alpha=.25, marker='.', s=[2],
#     color='#E048B8', zorder=3
# )
for i in range(len(lon)):
    (x, y) = mH(lon[i], lat[i])
    ax.annotate(i, xy=(x, y), size=.2, ha='center', va='center', color='white')
plo.quickSaveFig(PTH_PTS + 'raw.png', fig, dpi=1000)
mH.scatter(
    [i[0] for i in centroid], [i[1] for i in centroid], latlon=True,
    alpha=.5, marker='o', s=30,
    color='#233090', zorder=3
)
for i in range(CLS):
    (x, y) = mH(centroid[i][0], centroid[i][1])
    ax.annotate(i, xy=(x, y), size=5, ha='center', va='center')
plo.quickSaveFig(PTH_PTS + 'clusters.png', fig, dpi=1000)
# #############################################################################
# Kernel Heatmap
# #############################################################################
# kernel = np.genfromtxt(PTH_PTS + kernelName, delimiter=',')
# np.fill_diagonal(kernel, 0)
# fig = plt.figure(figsize=(5, 5))
# plt.imshow(kernel, interpolation='nearest', cmap='Purples', vmax=2e-04, vmin=0)
# fun.quickSaveFig(PTH_PTS + 'heat.png', fig, dpi=1000)
