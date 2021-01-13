
#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# /home/chipdelmal/miniconda3/envs/ox/lib/python3.7/site-packages/shapefile.py
# pip install matplotlib==3.2
###############################################################################

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


PTH_pts = '/home/chipdelmal/Documents/GitHub/MoNeT2/PYF/ONE/'
pts = pd.read_csv(PTH_pts+'data/Onetahi.csv', sep=',')
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
    '/home/chipdelmal/Documents/GitHub/MoNeT2/PYF/ONE/data/bh400kc3500', 
    'PYF', drawbounds=True, linewidth=15, color=COLORS[4], zorder=-1
)
mH.readshapefile(
    '/home/chipdelmal/Documents/GitHub/MoNeT2/PYF/ONE/data/bh400kc3500', 
    'PYF', drawbounds=True, linewidth=4, color=COLORS[0], zorder=2
)
mH.readshapefile(
    '/home/chipdelmal/Documents/GitHub/MoNeT2/PYF/ONE/data/bh400kc3500', 
    'PYF', drawbounds=True, linewidth=1, color=COLORS[3], zorder=2
)
# Buildings -------------------------------------------------------------------
mH.readshapefile(
    '/home/chipdelmal/Documents/GitHub/MoNeT2/PYF/ONE/data/Onetahi', 
    'One', drawbounds=True, linewidth=1, color=COLORS[1], zorder=3
)
patches   = []
for info, shape in zip(mH.One_info, mH.One):
    patches.append( Polygon(np.array(shape), True) )
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
    PTH_pts+'/images/ONE_map.png',
    dpi=DPI, facecolor='w', edgecolor=None,
    orientation='portrait', papertype=None, format='png',
    bbox_inches='tight', pad_inches=.02
)