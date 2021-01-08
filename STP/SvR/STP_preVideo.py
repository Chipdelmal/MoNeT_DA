
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
from joblib import Parallel, delayed
from os import path
from glob import glob
import STP_aux as aux
import STP_gene as drv
import STP_land as lnd
import STP_plots as plo
import STP_functions as fun
import STP_dataAnalysis as da
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#EXP = 'E_0025000000_03_0000000001_0100000000_0000000000'
EXP = sys.argv[5]
(USR, AOI, REL, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
(JOB, TMIN, TMAX) = (20, 0, 10*365)
EXP_NAM = '{}-{}'.format(EXP, AOI)
# #############################################################################
# Paths
# #############################################################################
EXP_NAM = '{}-{}'.format(EXP, AOI)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
AG_IDs = lnd.landSelector(LND, REL, PT_ROT)
(PT_UAS, PT_VID) = lnd.landPopSelector(REL, PT_ROT)
UA_sites = pd.read_csv(PT_UAS)
EXP_FLS = sorted(glob(path.join(PT_PRE, EXP_NAM + '*sum.bz')))
EXP_VID = path.join(PT_VID, EXP_NAM)
if len(EXP_FLS) == 0:
    print("Error: No experiment files were found!")
    sys.exit()
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
Parallel(n_jobs=JOB)(
    delayed(plo.plotMapFrame)(
        time, UA_sites, BLAT, BLNG, DRV_COL, GC_FRA, lngs, lats, EXP_VID,
        offset=1, amplitude=10, alpha=.35, marker=(6, 0)
    ) for time in range(TMIN, TMAX))
