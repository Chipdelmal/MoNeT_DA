

from os import path
import compress_pickle as pkl

###############################################################################
# Population
###############################################################################
(EXP, CLS) = ('E_0025000000_03_0000000000_0000000000_0000000000-HLT', '006')
PTH_P = '/home/chipdelmal/Documents/WorkSims/STP/SPA/265/PREPROCESS/'
dta = pkl.load(path.join(PTH_P, EXP+'_'+CLS+'_sum.bz'))
dta

dta['genotypes']
dta['population']

###############################################################################
# Clusters 
###############################################################################
FNM = 'clusters.bz'
PTH_G = '/home/chipdelmal/Documents/WorkSims/STP/SPA/GEO/cluster_1/'
pkl.load(path.join(PTH_G, FNM))