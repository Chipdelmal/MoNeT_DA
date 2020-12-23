
import os
import math
import glob
import numpy as np
import pandas as pd
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from os import path
from glob import glob
import STP_gene as drv
import STP_land as lnd
import STP_plots as plo
import STP_functions as fun
import STP_dataAnalysis as da


# #############################################################################
# Paths
# #############################################################################
PT_ROT = '/home/chipdelmal/Documents/WorkSims/STP/SPA/'
(UA_sites, PT_PRE, PT_VID) = (
    pd.read_csv(path.join(PT_ROT, 'GEO', 'cluster_1', 'stp_cluster_sites_pop_v5_fixed.csv')),
    path.join(PT_ROT, '265/PREPROCESS/'),
    path.join(PT_ROT, '265/video/')
)
EXP_NAM = 'E_0020000000_05_0000000100_0000000000_0000015730-HLT'
EXP_FLS = sorted(glob(path.join(PT_PRE, EXP_NAM + '*sum.bz')))
EXP_VID = path.join(PT_VID, EXP_NAM)
monet.makeFolder(PT_VID)
monet.makeFolder(EXP_VID)
# #############################################################################
# Pops counts
# #############################################################################
GC_RAW = [pkl.load(i)['population'] for i in EXP_FLS]
GC_FRA = [da.geneCountsToFractions(i) for i in GC_RAW]
DRV_COL = [i[:-2] for i in monet.COLHO]
# #############################################################################
# Geography
# #############################################################################
# Bounding box ----------------------------------------------------------------
(BLAT, BLNG) = ((-0.045, 1.75), (6.4, 7.5))
# LonLats and populations -----------------------------------------------------
(lonLat, pop) = (UA_sites[['lon', 'lat']], UA_sites['pop'])
# Landscape aggregation -------------------------------------------------------
AG_IDs = lnd.landSelector('SPA', '265', PT_ROT)
AGG_lonlats = [np.asarray([list(lonLat.iloc[i]) for i in j]) for j in AG_IDs]
AGG_centroids = da.aggCentroids(AGG_lonlats)
# #############################################################################
# Checks
# #############################################################################
popsMatch = len(GC_FRA) == len(AGG_lonlats)
print(popsMatch)
# #############################################################################
# Map
# #############################################################################
# Coordinates -----------------------------------------------------------------
(lngs, lats) = (AGG_centroids[:, 0], AGG_centroids[:, 1])
for time in range(GC_FRA[0].shape[0]):
    print('* Exporting {}'.format(str(time).zfill(4)), end='\r')
    # Create map --------------------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(10, 10))
    (fig, ax, mapR) = plo.plotMap(
        fig, ax, UA_sites, BLAT, BLNG, ptColor='#6347ff'
    )
    # Pops --------------------------------------------------------------------
    (fig, ax, mapR) = plo.plotGenePopsOnMap(
        fig, ax, mapR,
        lngs, lats, DRV_COL, 
        GC_FRA, time,
        marker=(6, 0), offset=5, amplitude=10, alpha=.5
    )
    ax.text(
        0.75, 0.1, str(time).zfill(4), 
        horizontalalignment='center', verticalalignment='center', 
        transform=ax.transAxes, fontsize=30
    )
    fun.quickSaveFig(
        '{}/{}.png'.format(EXP_VID, str(time).zfill(4)),
        fig, dpi=500
    )
    plt.close('all')