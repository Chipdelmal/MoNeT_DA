
import sys
from os import path
from datetime import datetime
from joblib import dump, load
import MoNeT_MGDrivE as monet
import plotly.express as px
import numpy as np
import pandas as pd
import PYF_aux as aux
from sklearn import preprocessing


if monet.isNotebook():
    (USR, LND, MTR, QNT, AOI) = ('dsk', 'PAN', 'WOP', '75', 'HLT')
else:
    (USR, LND, MTR, QNT) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

(FEATS, LABLS) = (['i_pop', 'i_ren', 'i_res', 'i_mad', 'i_mat'], ['0.1'])
###############################################################################
# Setting up paths
###############################################################################
ID_MTR = 'HLT_{}_{}_qnt.csv'.format(MTR, QNT)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR, PT_MOD) = aux.selectPath(
    USR, LND
)
PT_IMG = PT_IMG + 'pstModel/'
monet.makeFolder(PT_IMG)
tS = datetime.now()
monet.printExperimentHead(PT_DTA, PT_IMG, tS, 'PYF ClsExplore ')
###############################################################################
# Load Dataset
###############################################################################
df = pd.read_csv(path.join(PT_MTR, ID_MTR))
df['i_mos'] = (np.asarray(df['i_ren']) * np.asarray(df['i_res']))
cols = list(df.columns)
x = df.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df = pd.DataFrame(x_scaled, columns=cols)
###############################################################################
# Load Dataset
###############################################################################
fig = px.scatter_3d(
    df, x='i_mad', y='i_mat', z='i_ren',
    color='0.1', opacity=1
)
fig.show()


