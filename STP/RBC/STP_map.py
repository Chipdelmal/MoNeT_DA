
#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# /home/chipdelmal/miniconda3/envs/ox/lib/python3.7/site-packages/shapefile.py
# pip install matplotlib==3.2
# https://github.com/gboeing/osmnx-examples/blob/master/notebooks/10-building-footprints.ipynb
###############################################################################

from os import path
import matplotlib.pyplot as plt
import numpy as np
import STP_aux as aux
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PathCollection
from matplotlib.path import Path
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 1.0, 0.0, 0),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 1.0, 0),  # blue  with alpha = 20%
})
COLORS = [
    aux.rescaleRGBA((47, 28, 191, 255/2.5)),    # 0: Faded navy blue
    aux.rescaleRGBA((255, 0, 152, 255/1.75)),   # 1: Magenta
    aux.rescaleRGBA((37, 216, 17, 255/8)),      # 2: Bright green
    aux.rescaleRGBA((255, 255, 255, 255/1)),    # 3: White
    aux.rescaleRGBA((0, 169, 255, 255/7.5)),    # 4: Cyan
    aux.rescaleRGBA((0, 0, 0, 255/5))           # 5: Black
]

SHP = 'ne_10m_land_scale_rank'
PT_GEO = '/home/chipdelmal/Documents/WorkSims/STP_new/GEO/ne_10m'
PT_OUT = '/home/chipdelmal/Documents/WorkSims/STP_new/GEO/'
###############################################################################
# Map
###############################################################################
(minLat, minLong) = (-0.045, 6.4)
(maxLat, maxLong) = (.5, 6.85)
point = (np.mean([minLat, maxLat]), np.mean([minLong, maxLong]))
# #############################################################################
# Globe
# #############################################################################
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, label="1")
if SHP:
    map = Basemap(projection='ortho',lat_0=point[0]+0, lon_0=point[1]-20, resolution='c')
    shp_info = map.readshapefile(path.join(PT_GEO, SHP), 'scalerank', drawbounds=True)
    ax = plt.gca()
    ax.cla()
    paths = []
    for line in shp_info[4]._paths:
        paths.append(Path(line.vertices, codes=line.codes))
    coll = PathCollection(paths, linewidths=0, facecolors='grey', zorder=2)
else:
    map = Basemap(projection='ortho', lat_0=point[0]+0, lon_0=point[1]-0, ax=ax, resolution='c')
# map = Basemap(projection='geos', lon_0=-89.5, lat_0=0.0, satellite_height=45786023.0, ellps='GRS80')
map.drawmapboundary(color=COLORS[4], linewidth=15, zorder=5, ax=ax)
map.drawmapboundary(color=COLORS[0], linewidth=5, zorder=5, ax=ax)
map.drawmapboundary(color='#ffffff', linewidth=1, zorder=5, ax=ax)
pad = 500000
(limx, limy) = (ax.get_xlim(), ax.get_ylim())
ax.set_xlim(limx[0] - pad, limx[1] + pad)
ax.set_ylim(limy[0] - pad, limy[1] + pad)
# map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color=COLORS[0], lake_color=COLORS[3])
# map.drawcoastlines()
# map.drawcoastlines(color=COLORS[0], linewidth=0)
# map.drawcoastlines(color=COLORS[0], linewidth=2)
# map.drawcoastlines(color=COLORS[0], linewidth=0.25)
# map.drawparallels(np.arange(-90., 120., 30.), labels=[1,0,0,0], color='w', linewidth=.2)
# map.drawmeridians(np.arange(0., 420., 60.), labels=[0,0,0,1], color='w',  linewidth=.2)
(x, y) = map(point[1], point[0])
map.scatter(x, y, marker='o', color=COLORS[1], s=[75])
fig.savefig(
    PT_OUT+'STP_globe.png',
    dpi=500, facecolor='w', edgecolor=None,
    orientation='portrait', format='png',
    bbox_inches='tight', pad_inches=.02
)