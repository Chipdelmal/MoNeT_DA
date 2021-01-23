

import math
import shapely
import numpy as np
from random import shuffle
from os import path
import pandas as pd
import networkx as nx
import matplotlib
import cmasher as cmr
import matplotlib.pyplot as plt
import cdlib.algorithms as cd
from sklearn.preprocessing import normalize
from descartes import PolygonPatch
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
from networkx.algorithms import community, centrality
import STP_plots as pts
import STP_functions as fun


(PTH, LND) = ('/home/chipdelmal/Documents/WorkSims/STP/SPA/GEO/', 0)
COLORS = pts.COLORS
BASE_MAP = False
###############################################################################
# Select land
###############################################################################
if LND==0:
    # 265
    fldr = 'cluster_1'
    fname = ('kernel_cluster_v5.csv', 'stp_cluster_sites_pop_v5_fixed.csv')
elif LND==1:
    # 106
    fldr = 'cluster_2'
    fname = ('kernel_cluster_01_v5.csv', 'stp_cluster_sites_pop_01_v5_fixed.csv')
elif LND==2:
    # 505
    fldr = 'regular'
    fname = ('kernel_1_1029.csv', 'stp_all_sites_pop_v5_fixed.csv')
(PT_MTR, PT_PTS, PT_IMG) = (
    path.join(PTH, fldr, fname[0]),
    path.join(PTH, fldr, fname[1]),
    path.join(PTH, fldr)
)
###############################################################################
# Load
###############################################################################
psi = np.loadtxt(open(PT_MTR, "rb"), delimiter=",", skiprows=0)
points = pd.read_csv(PT_PTS)
longlats = points[['lon', 'lat']]
###############################################################################
# Pre process
###############################################################################
print('Diagonal: {}'.format(np.diagonal(psi)))
np.fill_diagonal(psi, 0)
pIn = np.sum(psi.T, axis=0)
print('ProbIn: {}'.format(pIn))
print('No access: {}'.format(list(np.where(pIn == 0)[0])))
psiN = normalize(psi, axis=1, norm='l2')
# (fig, ax) = pts.plotMatrix(psiN)
# fun.quickSave(fig, ax, PT_IMG, 'transitions.png', dpi=2000)
##############################################################################
# Transitions Matrix and Base Netowrk
##############################################################################
G = nx.from_numpy_matrix(psiN)
G.remove_edges_from(nx.selfloop_edges(G))
G = fun.calcNetworkDistance(G)
##############################################################################
# Community Detection
##############################################################################
coms = cd.markov_clustering(G)
comsID = coms.communities
ptsNum = points.shape[0]
labelsN = [fun.find_in_list_of_list(comsID, i)[0] for i in range(ptsNum)]
##############################################################################
# Geographic Clustering
##############################################################################
kmeans = AgglomerativeClustering(n_clusters=len(comsID)).fit(longlats)
labels = list(kmeans.labels_)
##############################################################################
# Plot
##############################################################################
(width, alpha) = (.5, 5)
cmap = matplotlib.cm.get_cmap('gist_rainbow', len(set(labels)))
cmapP = matplotlib.cm.get_cmap('cmr.chroma', len(set(labelsN)))
# shuffle(cmapP.colors)
(fig, ax) = plt.subplots(1, 1)
# Map -----------------------------------------------------------------------
xy = points[['lon', 'lat']]
pad = .1
(miny, minx) = (-0.045, 6.4)
(maxy, maxx) = (.5, 6.8)
# (minx, maxx) = (6.35, 7.55)
# (miny, maxy) = (-.1, 1.775)
mH = Basemap(
    projection='merc',
    llcrnrlat=miny, urcrnrlat=maxy,
    llcrnrlon=minx, urcrnrlon=maxx,
    lat_ts=20, resolution='h', ax=ax
)
mH.drawcoastlines(color=COLORS[0], linewidth=2, zorder=1)
mH.drawcoastlines(color=COLORS[3], linewidth=.25, zorder=2)
mL = Basemap(
    projection='merc',
    llcrnrlat=miny, urcrnrlat=maxy,
    llcrnrlon=minx, urcrnrlon=maxx,
    lat_ts=20, resolution='i', ax=ax
)
mL.drawcoastlines(color=pts.COLORS[4], linewidth=5, zorder=-5)
# Points --------------------------------------------------------------------
points['marker'] = 'o'
points['community'] = labelsN
points['color'] = [cmapP.colors[i] for i in points['community']]
if not BASE_MAP:
    cols = list(points['color'])
    fNameO = 'Coms.png'
else:
    cols = '#04011f'
    fNameO = 'Base.png'
mL.scatter(
    list(points['lon']), list(points['lat']), c=cols,
    marker='o', s=[1 + 1.75 * math.sqrt(i/100) for i in list(points['pop'])], 
    alpha=1, lw=.25, zorder=5, latlon=True, edgecolors='w'
)
ax.set_aspect(1)
ax.set_axis_off()
ax.axes.xaxis.set_ticklabels([])
ax.axes.yaxis.set_ticklabels([])
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
# Polygons -----------------------------------------------------------------
X = np.asarray(points[['lon', 'lat']])
if not BASE_MAP:
    r=.0225
    D = fun.disjoint_polygons(X, radius=r, n_angles=50)
    for j in list(set(labels)):
        matches = [key for key, val in enumerate(labels) if val in set([j])]
        base = D.geometry[matches[0]]
        for i in range(len(matches)):
            base = base.union(D.geometry[matches[i]].buffer(.01*r))
            mpoly = shapely.ops.transform(mH, base)
        ax.add_patch(
            PolygonPatch(
                mpoly, fc="none", ec='#6347ff', lw=1.5, alpha=.2, zorder=-3
            )
        )
        ax.add_patch(
            PolygonPatch(
                mpoly, fc="none", ec='#ffffff', lw=.5, alpha=1, zorder=-1
            )
        )
# Network ------------------------------------------------------------------
pts.plotNetworkOnMap(mL, psiN, X, X, c='#04011f', lw=.1)
fun.quickSave(fig, ax, PT_IMG, fNameO)