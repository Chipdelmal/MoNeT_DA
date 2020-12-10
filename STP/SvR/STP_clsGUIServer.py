from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput, RadioGroup, Button, FuncTickFormatter
from bokeh.plotting import figure, output_notebook, show
from bokeh.plotting import figure, output_file, save
from joblib import dump, load
import MoNeT_MGDrivE as monet
import numpy as np
import STP_classify as cls

MTR = 'WOP'
(FEATS, LABLS) = (
    ['i_smx', 'i_sgv', 'i_sgn', 'i_rsg', 'i_rer', 'i_ren', 'i_qnt', 'i_gsv', 'i_fic'],
    ['0.05']
)
###############################################################################
# Create directories structure
###############################################################################
ID_MTR = 'CLN_HLT_{}_{}_qnt.csv'.format(MTR, 'DM')
PT_ROT = '/home/chipdelmal/Documents/WorkSims/STP/PAN/'
(PT_IMG, PT_MOD, PT_OUT) = (
    PT_ROT+'img/', PT_ROT+'MODELS/', PT_ROT+'SUMMARY/'
)
ID_MTR = 'CLN_HLT_{}_{}_qnt.csv'.format(MTR, 'DM')
PTH_MOD = PT_MOD+ID_MTR[4:-10]+str(int(float(LABLS[0])*100)).zfill(2)+'_RF.joblib'
###############################################################################
# Load Model
###############################################################################
rf = load(PTH_MOD)
###############################################################################
# Create GUI
###############################################################################
qnt = Slider(title="Quantile", value=90, start=50, end=95, step=5)
rer = Slider(title="Released Fraction", value=.1, start=0, end=1.0, step=0.1)
ren = Slider(title="Release Number (weekly)", value=1, start=0, end=10, step=1)
fic = Slider(title="Fitness Cost", value=.25, start=0, end=1, step=.01)
rsg = TextInput(value="1e-5", title="Resistance Generation")
# rsg = Slider(title="Resistance Generation", start=0, end=.01, step=.0001, value=.001)
gsv = TextInput(value="1e-3", title="Genetic Standing Variation")
sex = RadioGroup(labels=["Male", "Gravid Female", "Non Gravid Female"], active=0)
btn = Button(label='Evaluate Model')
bto = Button(label='Output', disabled=True, button_type="success")


###############################################################################
# Testing Evaluation
#   'i_smx', 'i_sgv', 'i_sgn', 'i_rsg', 'i_rer', 'i_ren', 'i_qnt', 'i_gsv', 'i_fic
###############################################################################
def change_click():
    sexes = cls.sexTranslate(sex.active)
    inProbe = [[
        sexes[0], sexes[1], sexes[2], float(rsg.value), rer.value, 
        ren.value, qnt.value, gsv.value, fic.value
    ]]
    className = rf.predict(inProbe)
    pred = rf.predict_log_proba(inProbe)
    print("I: {}".format(inProbe))
    print("O: {} [{}]".format(className, pred[0]))
    bto.label='Protection Prediction: {}'.format(
        cls.labelTranslate(className[0])
    )
btn.on_click(change_click)
###############################################################################
# Generating layout
###############################################################################
output_notebook()
selectors = column(sex, rer, ren, fic, rsg, gsv, qnt, btn, bto)
curdoc().add_root(column(selectors))
output_file(PT_ROT+"test.html")
