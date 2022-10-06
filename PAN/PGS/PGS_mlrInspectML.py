
import sys
import shap
from os import path
import numpy as np
import pandas as pd
import compress_pickle as pkl
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from treeinterpreter import treeinterpreter as ti
import MoNeT_MGDrivE as monet
import PGS_aux as aux
import PGS_gene as drv


if monet.isNotebook():
    (USR, DRV, AOI, THS, MOI) = ('srv', 'PGS', 'HLT', '0.1', 'CPT')
else:
    (USR, DRV, AOI, THS, MOI) = sys.argv[1:]
# Setup number of threads -----------------------------------------------------
JOB = aux.JOB_DSK
if USR == 'srv':
    JOB = aux.JOB_SRV
CHUNKS = JOB
###############################################################################
# Paths
###############################################################################
(drive, land) = (
    drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE),
    aux.landSelector()
)
(gene, fldr) = (drive.get('gDict'), drive.get('folder'))
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, fldr)
PT_OUT = path.join(PT_ROT, 'ML')
PT_IMG = path.join(PT_OUT, 'img')
[monet.makeFolder(i) for i in [PT_OUT, PT_IMG]]
PT_SUMS = path.join(PT_ROT, 'SUMMARY')
# Time and head ---------------------------------------------------------------
tS = datetime.now()
monet.printExperimentHead(
    PT_ROT, PT_OUT, tS, 
    '{} mlrTrainML [{}:{}]'.format(DRV, AOI, THS)
)
###############################################################################
# Load Model from Disk
###############################################################################
fName = '{}_{}T_{}-MLR.pkl'.format(AOI, int(float(THS)*100), MOI)
rf = pkl.load(path.join(PT_OUT, fName))
###############################################################################
# Evaluate ML
###############################################################################
probeX = (
    ('ren', 48),
    ('rer', 48),
    ('rei', 8),
    ('pct', 0.0),
    ('pmd', 1.0),
    ('mfr', 0.0),
    ('mtf', 1.0),
    ('fvb', 0.0),
)
FEATS = [i[0] for i in probeX]
# Evaluate models at probe point ----------------------------------------------
vct = np.array([[i[1] for i in probeX]])
# pred = rf.predict(vct)
(prediction, bias, contributions) = ti.predict(rf, vct)
# -----------------------------------------------------------------------------
print("* Predicted: {}".format(prediction[0][0]))
print("\tBias: {}".format(bias[0]))
for (c, feature, inVal) in zip(contributions[0], FEATS, vct[0]):
    ptest = '{:.4f}'.format(c).zfill(3)
    print('\t{} ({:.2f}): {}'.format(feature, inVal, ptest))


rWidth = 1
(bias, contributions) = (bias, contributions)

(bs, cntr) = (bias[0], contributions[0])
(fig, ax) = plt.subplots(figsize=(10, 10))
ax.add_patch(Rectangle((bias, 0), bs+cntr[0], 1))
ax.set_xlim(-2, 2)
ax.set_ylim(0, 4)