
from os import path
import STP_aux as aux
import compress_pickle as pkl

USR = 'lab'

PTH_ROT = aux.selectPathGeo(USR)
(SOUTH, SITES, SPLIT_ISLAND) = (aux.SOUTH, aux.SITES, 27)

###############################################################################
# Load full data
###############################################################################
dta = pkl.load(path.join(PTH_ROT, 'clusters_002.bz'))
sitesNum = max([max(i) for i in dta])
NO_ACCESS = {51, 239}
PRINCIPE = set(range(SPLIT_ISLAND))
SAOTOME = (set(range(sitesNum))-NO_ACCESS)-PRINCIPE
###############################################################################
# Split
###############################################################################
southRel = [list(SAOTOME-set(SOUTH)), SOUTH, list(NO_ACCESS), list(PRINCIPE)]
sitesRel = [list(SAOTOME-set(SITES)), SITES, list(NO_ACCESS), list(PRINCIPE)]
###############################################################################
# Dump data lists
###############################################################################
pkl.dump(southRel, PTH_ROT+'clusters_0DR', compression='bz2')
pkl.dump(sitesRel, PTH_ROT+'clusters_0SR', compression='bz2')