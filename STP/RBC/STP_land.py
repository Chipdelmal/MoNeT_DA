#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import compress_pickle as pkl
import STP_aux as aux


def landSelector(EXP, LND, USR='lab'):
    if (LND=='PAN'):
        PAN = ([0], )
        return PAN
    else:
        if (EXP=='265_SP') or (EXP=='265_DP'):
            PT = aux.selectPathGeo(USR)
            PAN = pkl.load(path.join(PT, 'clusters_002.bz'))
            return PAN
        elif (EXP=='265_SS') or (EXP=='265_DS'):
            PT = aux.selectPathGeo(USR)
            SPA = pkl.load(path.join(PT, 'clusters_020.bz'))
            return SPA



# def landPopSelector(REL, PT_ROT):
#     if (REL=='265') or (REL=='265P'):
#         PT_UAS = path.join(
#             ''.join(PT_ROT.split('/'+REL)).replace('/sim/', ''),
#             'GEO', 'cluster_1', 'stp_cluster_sites_pop_v5_fixed.csv'
#         )
#     return (PT_UAS, path.join(PT_ROT, 'video'))



