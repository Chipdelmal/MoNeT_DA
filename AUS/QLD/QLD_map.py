
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import QLD_functions as fun
import QLD_plots as plo
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D


plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 1.0, 0.0, 0),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 1.0, 0),  # blue  with alpha = 20%
})


PTH_pts = '/home/chipdelmal/Documents/WorkSims/QLD/GEO/'
pts = pd.read_csv(PTH_pts+'MurWon_BlockCentroids.txt', sep='\t')
(COLORS, DPI) = (plo.COLORS, 300)
# #############################################################################
# Map
# #############################################################################
PAD = .01
(minLat, minLong) = [i-PAD for i in (-26.32779192, 151.8641686)]
(maxLat, maxLong) = [i+PAD for i in (-26.23022147, 151.9552239)]
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
# Geography -------------------------------------------------------------------
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
# Pointsets -------------------------------------------------------------------
zoneNames = sorted(list(pts['FolderPath'].unique()))
(murgonPts, wondaiPts) = [pts[pts['FolderPath']==i] for i in zoneNames]
mH.scatter(
    list(murgonPts['Xcoord']), list(murgonPts['Ycoord']), latlon=True,
    alpha=.3, marker='.', 
    s=[25 * math.log(10000000*i) for i in list(pts['Shape_Area'])],
    color='#E048B8', zorder=3
)
mH.scatter(
    list(wondaiPts['Xcoord']), list(wondaiPts['Ycoord']), latlon=True,
    alpha=.3, marker='.', 
    s=[25 * math.log(10000000*i) for i in list(pts['Shape_Area'])],
    color='#233090', zorder=3
)
fig.savefig(
    PTH_pts+'QLD_map.png',
    dpi=DPI, facecolor='w', edgecolor=None,
    orientation='portrait', papertype=None, format='png',
    bbox_inches='tight', pad_inches=.02
)
# #############################################################################
# Globe
# #############################################################################
(x1, y1) = (151.8641686, -26.32779192)
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
map = Basemap(projection='ortho', lat_0=y1, lon_0=x1-20, ax=ax, resolution='c')
# map = Basemap(projection='geos', lon_0=-89.5, lat_0=0.0, satellite_height=45786023.0, ellps='GRS80')
map.drawmapboundary(color='#141b52', linewidth=5, zorder=5, ax=ax)
pad = 500000
(limx, limy) = (ax.get_xlim(), ax.get_ylim())
ax.set_xlim(limx[0] - pad, limx[1] + pad)
ax.set_ylim(limy[0] - pad, limy[1] + pad)
# map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='#141b52', lake_color='#233090')
# map.drawcoastlines()
map.drawcoastlines(color='#141b52', linewidth=0)
# map.drawcoastlines(color=COLORS[0], linewidth=2)
map.drawcoastlines(color='#141b52', linewidth=0.25)
# map.drawparallels(np.arange(-90., 120., 30.), labels=[1,0,0,0], color='w', linewidth=.2)
# map.drawmeridians(np.arange(0., 420., 60.), labels=[0,0,0,1], color='w',  linewidth=.2)
(x, y) = map(x1, y1)
map.plot(x, y, marker='o', color="#e048b8F5")
fig.savefig(
    PTH_pts+'QLD_globe.png',
    dpi=DPI, facecolor='w', edgecolor=None,
    orientation='portrait', papertype=None, format='png',
    bbox_inches='tight', pad_inches=.02
)