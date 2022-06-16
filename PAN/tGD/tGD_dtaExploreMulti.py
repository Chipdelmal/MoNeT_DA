from pydoc import render_doc
import sys
from os import path
from re import match
from glob import glob
from joblib import dump, load
from datetime import datetime
import numpy as np
from numpy.lib.arraypad import pad
import pandas as pd
from joblib import Parallel, delayed
import MoNeT_MGDrivE as monet
import tGD_aux as aux
import tGD_gene as drv
from more_itertools import locate
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

if monet.isNotebook():
    (USR, DRV, AOI, QNT, THS) = ('srv2', 'tGD', ('HLT', 'TRS'), '50', ('0.25', '0.25'))
else:
    (USR, DRV, AOI, QNT, THS) = sys.argv[1:]
EXPS = aux.EXPS
exp = EXPS[0]
# Setup number of cores -------------------------------------------------------
if USR=='dsk':
    JOB = aux.JOB_DSK
else:
    JOB = aux.JOB_SRV
###############################################################################
# Paths
###############################################################################
(drive, land) = (drv.driveSelector(DRV, AOI[0], popSize=aux.POP_SIZE), [[0], ])
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)
PT_ROT = path.split(path.split(PT_ROT)[0])[0]
PT_OUT = path.join(PT_ROT, 'ML')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, exp, 'SUMMARY')
###############################################################################
# Read CSV
###############################################################################
thsStr = [str(int(float(ths)*100)) for ths in THS]
fName_I = ['SCA_{}_{}Q_{}T.csv'.format(aoi, QNT, ths) for (aoi, ths) in zip(AOI, thsStr)]
(DATA_H, DATA_T) = [pd.read_csv(path.join(PT_OUT, name)) for name in fName_I]
# Features and labels ---------------------------------------------------------
COLS = list(DATA_H.columns)
(FEATS, LABLS) = (
    [i for i in COLS if i[0]=='i'], [i for i in COLS if i[0]!='i']
)
# Time and head --------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_OUT, PT_OUT, tS,
    '{} DtaExplore [{}:{}:{}:{}]'.format('tGD', DRV, QNT, AOI, THS)
)
###############################################################################
# Filter Output with Constraints
###############################################################################
# Both ------------------------------------------------------------------------
(renRge, resRge) = ((-1, 20), (-1, 1))
# HLT (gRNA) ------------------------------------------------------------------
wopRge = (0, 10*365)
fltrA = (
    renRge[0] <= DATA_H['i_ren'], DATA_H['i_ren'] <= renRge[1],
    resRge[0] <= DATA_H['i_res'], DATA_H['i_res'] <= resRge[1],
    wopRge[0] <= DATA_H['WOP'],   DATA_H['WOP']   <= wopRge[1],
)
fullFltrA = list(map(all, zip(*fltrA)))
# TRS (Cas9) ------------------------------------------------------------------
wopRge = (20, 300)
fltrB = (
    renRge[0] <= DATA_T['i_ren'],   DATA_T['i_ren'] <= renRge[1],
    resRge[0] <= DATA_T['i_res'],   DATA_T['i_res'] <= resRge[1],
    wopRge[0] <= DATA_T['WOP'],     DATA_T['WOP']   <= wopRge[1],
)
fullFltrB = list(map(all, zip(*fltrB)))
# Put them together -----------------------------------------------------------
fullFltr = list(map(all, zip(fullFltrA, fullFltrB)))
print('* Matches found: {}'.format(sum(fullFltr)))
DATA_FILTERED = [dta[fullFltr] for dta in (DATA_H, DATA_T)]
###############################################################################
# Export data
###############################################################################
DATA_FILTERED[0].to_csv(path.join(PT_OUT, 'DTA_FLTR_{}.csv'.format(AOI[0])), index=False)
DATA_FILTERED[1].to_csv(path.join(PT_OUT, 'DTA_FLTR_{}.csv'.format(AOI[1])), index=False)
