
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
import STP_auxDebug as dbg
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

if monet.isNotebook():
    (USR, AOI, LND, DRV, exp) = ('lab', 'HLT', 'SPA', 'LDR', '265_SS')
    EXP = 'E_01_12_00500_000790000000_000100000000_0017500_0011700_0000000_0100000_0095600'
    JOB = aux.JOB_DSK
else:
    (USR, AOI, LND, DRV, exp) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    EXP = sys.argv[6]
    JOB = aux.JOB_SRV
(TMIN, TMAX) = (1, 5*365)
###############################################################################
# Processing loop
###############################################################################
EXPS = aux.getExps(LND)
###########################################################################
# Setting up paths
###########################################################################
EXP_NAM = '{}-{}'.format(EXP, AOI)
(drive, AG_IDs) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    lnd.landSelector(exp, LND, USR=USR)
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
    USR, exp, LND, DRV
)
PT_VID = path.join(PT_IMG, 'preVideo')
EXP_VID = path.join(PT_VID, EXP_NAM)
PT_UAS = path.join(
    '/'.join(
        PT_ROT.split('/')[:-4]+
        ['GEO', 'cluster_1', 'stp_cluster_sites_pop_v5_fixed.csv']
    )
)
UA_sites = pd.read_csv(PT_UAS)
[monet.makeFolder(i) for i in [PT_VID, EXP_VID]]
###############################################################################
# Read data
###############################################################################
EXP_FLS = sorted(glob(path.join(PT_PRE, EXP_NAM + '*sum.bz')))
if len(EXP_FLS) == 0:
    print("Error: No experiment files were found!")
    sys.exit()
GC_RAW = [pkl.load(i)['population'] for i in EXP_FLS]
GC_FRA = [dbg.geneCountsToFractions(i) for i in GC_RAW]
DRV_COL = [i[:-2] for i in drv.colorSelector(AOI)]
# #############################################################################
# Geography
# #############################################################################
# Bounding box ----------------------------------------------------------------
# (BLAT, BLNG) = ((-0.045, 1.75), (6.4, 7.5))
(BLAT, BLNG) = ((-0.045, .5), (6.4, 6.8))
# LonLats and populations -----------------------------------------------------
(lonLat, pop) = (UA_sites[['lon', 'lat']], UA_sites['pop'])
# Landscape aggregation -------------------------------------------------------
AGG_lonlats = [np.asarray([list(lonLat.iloc[i]) for i in j]) for j in AG_IDs]
AGG_centroids = dbg.aggCentroids(AGG_lonlats)
# #############################################################################
# Checks
# #############################################################################
popsMatch = len(GC_FRA) == len(AGG_lonlats)
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(PT_ROT, PT_VID, tS, 'STP PreVideo '+AOI)
# #############################################################################
# Map
# #############################################################################
# Coordinates -----------------------------------------------------------------
(lngs, lats) = (AGG_centroids[:, 0], AGG_centroids[:, 1])
Parallel(n_jobs=JOB)(
    delayed(dbg.plotMapFrame)(
        time, UA_sites, BLAT, BLNG, DRV_COL, GC_FRA, lngs, lats, EXP_VID,
        offset=1, amplitude=90, alpha=.5, marker=(6, 0), edgecolor='#ffffff55'
    ) for time in range(TMIN, TMAX))
