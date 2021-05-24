
import numpy as np
from os import path
import pandas as pd
import seaborn as sns
import compress_pickle as pkl
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from descartes import PolygonPatch
from more_itertools import locate
import QLD_fun as fun
import QLD_aux as aux

CLS_NUM = 10
(PTH_PTS, FNM_PTS) = (
    aux.selectGeoPath('dsk'), 
    'MurWon_BlockCentroids'
)
FNM_OUT = '{}_C{}.csv'.format(FNM_PTS, str(CLS_NUM).zfill(2))
###############################################################################
# Read Geo-Data
###############################################################################
df = pd.read_csv(path.join(PTH_PTS, FNM_PTS+'.txt'), sep='\t')
lonLat = list(zip(df['Xcoord'], df['Ycoord']))
kmeans = KMeans(n_clusters=CLS_NUM, random_state=7415341).fit(lonLat)
df['clst'] = kmeans.labels_
centroids = kmeans.cluster_centers_
df['id'] = range(df.shape[0])
df.to_csv(path.join(PTH_PTS, FNM_OUT))
###############################################################################
# Plot Clusters
###############################################################################
(X, CLS_LB) = (np.asarray(lonLat), df['clst'])
# Clusters --------------------------------------------------------------------
(fig, ax) = plt.subplots(1, 1)
plt.scatter(
    df['Xcoord'], df['Ycoord'], marker='o',
    color='#03045e55', s=1.5
)
for i in range(df.shape[0]):
    plt.text(
        df['Xcoord'].iloc[i], df['Ycoord'].iloc[i], str(i), 
        color='#ffffffAA', fontsize=1.25, ma='center', ha='center', va='center'
    )
for i in range(len(centroids)):
    plt.text(
        centroids[i][0], centroids[i][1], str(i), 
        color='#00000022', fontsize=12.5, zorder=-1,
        ma='center', ha='center', va='center'
    )
# Polygons --------------------------------------------------------------------
D = fun.disjoint_polygons(X, radius=.0075, n_angles=3)
for j in list(set(CLS_LB)):
    matches = [key for key, val in enumerate(CLS_LB) if val in set([j])]
    base = D.geometry[matches[0]]
    for i in range(len(matches)):
        base = base.union(D.geometry[matches[i]].buffer(0.00005))
    ax.add_patch(
        PolygonPatch(
            base, fc="none", ec='#6347ff', lw=1, alpha=.2, zorder=10
        )
    )
    ax.add_patch(
        PolygonPatch(
            base, fc="none", ec='#ffffff', lw=.1, alpha=1, zorder=10
        )
    )
ax.set_aspect(1)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(
    axis='both', which='both',
    bottom=False, top=False, left=False, right=False,
    labelbottom=False, labelleft=False
)
fig.savefig(
    path.join(PTH_PTS, 'Map{}.png'.format(str(CLS_NUM).zfill(2))), 
    dpi=1000, edgecolor=None,
    orientation='portrait', papertype=None, format='png',
    bbox_inches='tight', pad_inches=.02
)
###############################################################################
# Export groupings by ID
###############################################################################
groupings = []
clstIDs = list(sorted(set(df['clst'])))
for (ix, clstID) in enumerate(clstIDs):
    tmpDF = df[df['clst'] == clstID]
    groupings.append(list(tmpDF['id']))
out = {
    'centroid': kmeans.cluster_centers_,
    'groups': groupings
}
pkl.dump(
    out, path.join(PTH_PTS, 'CLS_{}.pkl'.format(str(CLS_NUM).zfill(2))), 
    compression='bz2'
)