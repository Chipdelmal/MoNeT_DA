
from os import path
import compress_pickle as pkl


def landSelector(land, PT_ROT):
    if land == 'PAN':
        lnd = (list(range(0, 62)), )
        return lnd
    else:
        pth = ''.join(PT_ROT.replace('/sims/'+land+'/', ''))
        lnd = pkl.load(path.join(pth, 'GEO', 'clusters.bz'))
        return lnd
