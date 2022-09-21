
import sys
from os import path
import numpy as np
from numpy import full
import pandas as pd
from functools import reduce
from datetime import datetime
import MoNeT_MGDrivE as monet
import PGS_aux as aux
import PGS_gene as drv
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor
from gp_extras.kernels import HeteroscedasticKernel
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel as C
from sklearn.cluster import KMeans
from sklearn.linear_model import QuantileRegressor


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
# Read Dataframe
###############################################################################
fName = 'SCA_{}_{}T_MLR.csv'.format(AOI, int(float(THS)*100))
df = pd.read_csv(path.join(PT_OUT, fName))
###############################################################################
# Split I/O
###############################################################################
indVars = [i[0] for i in aux.DATA_HEAD]
dfIn = df[indVars].drop('i_grp', axis=1)
(X, y) = (np.array(dfIn), np.array(df[MOI]))
(X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size=0.975)
###############################################################################
# Train Model
###############################################################################
# kernel_homo = C(1.0, (1e-10, 1000)) * RBF(1, (0.01, 100.0)) + WhiteKernel(1e-3, (1e-10, 50.0))
# gp_homoscedastic = GaussianProcessRegressor(kernel=kernel_homo, alpha=0)
# gp_homoscedastic.fit(X_train[:], y_train[:])
# gp_homoscedastic.log_marginal_likelihood(gp_homoscedastic.kernel_.theta)


qr = QuantileRegressor(quantile=0.5, alpha=0)
y_pred = qr.fit(X_train, y_train).predict(X)
