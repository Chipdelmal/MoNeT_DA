
import os
import sys
import math
import glob
import numpy as np
import pandas as pd
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
from os import path
from glob import glob
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_plots as plo
import STP_functions as fun
import STP_dataAnalysis as da


EXP = 'E_0020000000_03_0000000100_0100000000_0000015730'
(USR, AOI, REL, LND) = ('dsk', 'HLT', '265', 'SPA')
# (USR, AOI, REL, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
tmax = 2 * 365
EXP_NAM = '{}-{}'.format(EXP, AOI)
# #############################################################################
# Paths
# #############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
AG_IDs = lnd.landSelector(LND, REL, PT_ROT)
(PT_UAS, PT_VID) = lnd.landPopSelector(REL, PT_ROT)
UA_sites = pd.read_csv(PT_UAS)
EXP_FLS = sorted(glob(path.join(PT_PRE, EXP_NAM + '*sum.bz')))
EXP_VID = path.join(PT_VID, EXP_NAM)
monet.makeFolder(PT_VID)
monet.makeFolder(EXP_VID)
# #############################################################################
# Pops counts
# #############################################################################
GC_RAW = [pkl.load(i)['population'] for i in EXP_FLS]
GC_FRA = [da.geneCountsToFractions(i) for i in GC_RAW]
DRV_COL = [i[:-2] for i in drv.colorSelector(AOI)]
# #############################################################################
# Geography
# #############################################################################
# Bounding box ----------------------------------------------------------------
(BLAT, BLNG) = ((-0.045, 1.75), (6.4, 7.5))
# LonLats and populations -----------------------------------------------------
(lonLat, pop) = (UA_sites[['lon', 'lat']], UA_sites['pop'])
# Landscape aggregation -------------------------------------------------------
AGG_lonlats = [np.asarray([list(lonLat.iloc[i]) for i in j]) for j in AG_IDs]
AGG_centroids = da.aggCentroids(AGG_lonlats)
# #############################################################################
# Checks
# #############################################################################
popsMatch = len(GC_FRA) == len(AGG_lonlats)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_ROT, PT_VID, tS, 'UCIMI PreVideo '+AOI)
# #############################################################################
# Map
# #############################################################################
# Coordinates -----------------------------------------------------------------
(lngs, lats) = (AGG_centroids[:, 0], AGG_centroids[:, 1])
for time in range(tmax): # range(GC_FRA[0].shape[0]):
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
        marker=(6, 0), offset=2.5, amplitude=5, alpha=.35
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