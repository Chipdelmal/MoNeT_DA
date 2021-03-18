
import sys
from os import path
from datetime import datetime
from joblib import dump, load
import MoNeT_MGDrivE as monet
import plotly.express as px
import numpy as np
import pandas as pd
import STP_aux as aux
from sklearn import preprocessing
import plotly.graph_objects as go


if monet.isNotebook():
    (MTR, QNT) = ('CPT', '50')
    LABLS = ['CPT']
else:
    (MTR, QNT) = (sys.argv[1], sys.argv[2])
    LABLS = ['0.5']
FEATS = [
        'i_smx', 'i_sgv', 'i_sgn',
        'i_rsg', 'i_rer', 'i_ren', 'i_qnt', 'i_gsv', 'i_fic'
    ]   
###############################################################################
# Create directories structure
###############################################################################
ID_MTR = 'CLN_HLT_{}_{}_qnt.csv'.format(MTR, QNT)
PT_ROT = '/home/chipdelmal/Documents/WorkSims/STP/PAN/'
(PT_IMG, PT_MOD, PT_OUT) = (
    PT_ROT+'img/', PT_ROT+'MODELS/', PT_ROT+'SUMMARY/'
)
ID_MTR = 'CLN_HLT_{}_{}_qnt.csv'.format(MTR, QNT)
if MTR == 'CPT':
    PTH_MOD = PT_MOD+ID_MTR[0][4:-8]+'_RF.joblib'
else:
    PTH_MOD = PT_MOD+ID_MTR[4:-10]+str(int(float(LABLS[0])*100))+'_RF.joblib'
###############################################################################
# Load Dataset
###############################################################################
df = pd.read_csv(path.join(PT_OUT, ID_MTR))
cols = ('i_rsg', 'i_rer', 'i_ren', 'i_qnt', 'i_gsv', 'i_fic', LABLS[0])
x = df[[*cols]].values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df = pd.DataFrame(x_scaled, columns=cols)
gsv = list(df['i_gsv'].unique())
dfFltrd = df[df['i_gsv']==gsv[-1]]
###############################################################################
# Load Dataset
###############################################################################
fig = px.scatter_3d(
    dfFltrd, 
    x='i_rer', y='i_ren', z='i_fic', 
    size=list(1*np.asarray(dfFltrd['i_rsg'])),
    color=LABLS[0], 
    opacity=.25, color_continuous_scale='purples_r'
)
fig.update_traces(
    marker=dict(
        # size=2, 
        line=dict(width=0, color=(0,0,0,0))
    )
)
fig.show()
