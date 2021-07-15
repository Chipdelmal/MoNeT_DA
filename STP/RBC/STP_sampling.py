
from os import path
import pandas as pd
from glob import glob
import STP_aux as aux
import MoNeT_MGDrivE as monet

from skopt.space import Space
from skopt.sampler import Lhs


space = Space([
    (0.0395, 0.0790, 0.1185, 0.0000), 
    (0, 1e-2, 1e-4, 1e-8), 
    (0.08750, 0.13125, 0.17500, 0.21875, 0.26250, 0.00000)
])

n_samples = 100

rand = space.rvs(NSAMP)
len(rand)


lhs = Lhs(lhs_type="centered", criterion=None)
lhs.generate(space.dimensions, n_samples)

# if monet.isNotebook():
#     (USR, LND) = ('dsk', 'PAN')
# else:
#     (USR, LND) = (sys.argv[1], sys.argv[2])
# EXPS = aux.getExps(LND)
# (PT_ROT, _, _, _, _, _) = aux.selectPath(USR, EXPS[0], LND)
# expsToPlot = aux.EXPS_TO_PLOT
###############################################################################
# Generate keycards
###############################################################################
# kCats = [i[0] for i in aux.DATA_HEAD]
# scalers = [aux.DATA_SCA[i] for i in kCats]
# splitExps = [i.split('_')[1:] for i in expsToPlot]
# keyCards = [
#     {
#         kCats[ix]: int(k)/i for (ix, (k, i)) in enumerate(zip(sExp, scalers))
#     } for sExp in splitExps
# ]
# expsKeysDF = pd.DataFrame.from_dict(keyCards)
# expsKeysDF.to_csv(path.join(PT_ROT, 'TracesKey.csv'), index=False)