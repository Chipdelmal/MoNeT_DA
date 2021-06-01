
from os import path
import pandas as pd
from glob import glob
import STP_aux as aux
import MoNeT_MGDrivE as monet

if monet.isNotebook():
    (USR, LND) = ('dsk', 'PAN')
else:
    (USR, LND) = (sys.argv[1], sys.argv[2])
EXPS = aux.getExps(LND)
(PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND)
expsToPlot = aux.EXPS_TO_PLOT
###############################################################################
# Generate keycards
###############################################################################
kCats = [i[0] for i in aux.DATA_HEAD]
scalers = [aux.DATA_SCA[i] for i in kCats]
splitExps = [i.split('_')[1:] for i in expsToPlot]
keyCards = [
    {
        kCats[ix]: int(k)/i for (ix, (k, i)) in enumerate(zip(sExp, scalers))
    } for sExp in splitExps
]
expsKeysDF = pd.DataFrame.from_dict(keyCards)
expsKeysDF.to_csv(path.join(PT_ROT, 'TracesKey.csv'), index=False)