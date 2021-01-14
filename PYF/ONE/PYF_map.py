
#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# /home/chipdelmal/miniconda3/envs/ox/lib/python3.7/site-packages/shapefile.py
# pip install matplotlib==3.2
# https://github.com/gboeing/osmnx-examples/blob/master/notebooks/10-building-footprints.ipynb
###############################################################################

import os
import math
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import PYF_aux as aux
import PYF_plots as plo
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 1.0, 0.0, 0),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 1.0, 0),  # blue  with alpha = 20%
})

(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath('dsk', 'Onetahi', 'temp')
PTH_pts = '/'.join(PT_ROT.split('/')[:-2]) + '/GEO/'
SHPFS = ('bh400kc3500', 'Onetahi')
pts = pd.read_csv(PTH_pts+'Onetahi.csv', sep=',')
(COLORS, DPI) = (plo.COLORS, 500)
###############################################################################
# Map
###############################################################################
PAD = .00675
point = (-17.0187975, -149.591045)
# (minLat, minLong) = [i-PAD for i in (min(list(pts['lats'])), min(list(pts['lons'])))]
# (maxLat, maxLong) = [i+PAD for i in (max(list(pts['lats'])), max(list(pts['lons'])))]
(minLat, minLong) = [i-PAD for i in point]
(maxLat, maxLong) = [i+PAD for i in point]
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
###############################################################################
# Get footprints
###############################################################################
# Geography -------------------------------------------------------------------
mH = Basemap(
    projection='merc', lat_ts=20, resolution='h', ax=ax,
    llcrnrlat=minLat, urcrnrlat=maxLat, llcrnrlon=minLong, urcrnrlon=maxLong   
)
mH.readshapefile(
    PTH_pts+SHPFS[0], 'PYF', 
    drawbounds=True, linewidth=15, color=COLORS[4], zorder=-1
)
mH.readshapefile(
    PTH_pts+SHPFS[0], 'PYF', 
    drawbounds=True, linewidth=4, color=COLORS[0], zorder=2
)
mH.readshapefile(
    PTH_pts+SHPFS[0], 'PYF', 
    drawbounds=True, linewidth=1, color=COLORS[3], zorder=2
)
# Buildings -------------------------------------------------------------------
mH.readshapefile(
    PTH_pts+SHPFS[1], 'One', 
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
# Centroids -------------------------------------------------------------------
# mH.scatter(
#     list(pts['lons']), list(pts['lats']), latlon=True,
#     alpha=.1, marker='.', 
#     s=.1, color='#233090', zorder=3
# )
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
# Save figure -----------------------------------------------------------------
fig.savefig(
    PTH_pts+'/ONE_map.png',
    dpi=DPI, facecolor='w', edgecolor=None,
    orientation='portrait', papertype=None, format='png',
    bbox_inches='tight', pad_inches=.02
)
# #############################################################################
# Globe
# #############################################################################
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
map = Basemap(projection='ortho', lat_0=point[0]+20, lon_0=point[1]+30, ax=ax, resolution='c')
# map = Basemap(projection='geos', lon_0=-89.5, lat_0=0.0, satellite_height=45786023.0, ellps='GRS80')
map.drawmapboundary(color='#141b52', linewidth=5, zorder=5, ax=ax)
pad = 500000
(limx, limy) = (ax.get_xlim(), ax.get_ylim())
ax.set_xlim(limx[0] - pad, limx[1] + pad)
ax.set_ylim(limy[0] - pad, limy[1] + pad)
# map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='#141b52', lake_color='#141b52')
# map.drawcoastlines()
map.drawcoastlines(color='#141b52', linewidth=0)
# map.drawcoastlines(color=COLORS[0], linewidth=2)
map.drawcoastlines(color='#141b52', linewidth=0.25)
# map.drawparallels(np.arange(-90., 120., 30.), labels=[1,0,0,0], color='w', linewidth=.2)
# map.drawmeridians(np.arange(0., 420., 60.), labels=[0,0,0,1], color='w',  linewidth=.2)
(x, y) = map(point[1], point[0])
map.plot(x, y, marker='o', color="#e048b8F5")
fig.savefig(
    PTH_pts+'PYF_globe.png',
    dpi=DPI, facecolor='w', edgecolor=None,
    orientation='portrait', papertype=None, format='png',
    bbox_inches='tight', pad_inches=.02
)