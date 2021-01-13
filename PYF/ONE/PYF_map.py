
#!/usr/bin/python
# -*- coding: utf-8 -*-
# /home/chipdelmal/miniconda3/envs/MoNeT/lib/python3.7/site-packages/shapefile.py

import os
import math
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
# import QLD_functions as fun
import PYF_plots as plo
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D


plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 1.0, 0.0, 0),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 1.0, 0),  # blue  with alpha = 20%
})


PTH_pts = '/home/chipdelmal/Documents/GitHub/MoNeT2/PYF/ONE/'
pts = pd.read_csv(PTH_pts+'data/Onetahi.csv', sep=',')
(COLORS, DPI) = (plo.COLORS, 300)
###############################################################################
# Map
###############################################################################
PAD = .01
(minLat, minLong) = [i-PAD for i in (min(list(pts['lats'])), min(list(pts['lons'])))]
(maxLat, maxLong) = [i+PAD for i in (max(list(pts['lats'])), max(list(pts['lons'])))]
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
mH.drawcoastlines(color=COLORS[0], linewidth=.25, zorder=2)
mL = Basemap(
    projection='merc',
    llcrnrlat=minLat, urcrnrlat=maxLat,
    llcrnrlon=minLong, urcrnrlon=maxLong,
    lat_ts=20, resolution='i', ax=ax
)
mL.drawcoastlines(color=COLORS[0], linewidth=10, zorder=0)
ax.tick_params(
    axis='both', which='both',
    bottom=True, top=False, left=True, right=False,
    labelbottom=True, labelleft=True
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
mH.readshapefile(
    '/home/chipdelmal/Documents/GitHub/MoNeT2/PYF/ONE/data/bh400kc3500', 
    'PYF',
    default_encoding='latin-1'
)
# Pointsets -------------------------------------------------------------------
mH.scatter(
    list(pts['lons']), list(pts['lats']), latlon=True,
    alpha=.3, marker='.', 
    s=10,
    color='#233090', zorder=3
)
fig.savefig(
    PTH_pts+'/images/ONE_map.png',
    dpi=DPI, facecolor='w', edgecolor=None,
    orientation='portrait', papertype=None, format='png',
    bbox_inches='tight', pad_inches=.02
)