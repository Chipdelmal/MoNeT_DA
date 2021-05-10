#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import compress_pickle as pkl

def landSelector(EXP, LND):
    if (LND=='PAN'):
        PAN = ([0], )
        return PAN

    # if (EXP == '265'):
    #     pth = ''.join(PT_ROT.split('/'+REL)).replace('/sim/', '')
    #     STP = pkl.load(pth+ '/GEO/cluster_1/clusters.bz')
    # elif (EXP == '265'):
    #     pth = ''.join(PT_ROT.split('/'+REL)).replace('/sim/', '')
    #     STP = pkl.load(pth+ '/GEO/cluster_1/SPAN/clusters.bz')
    #     # Return --------------------------------------------------------------
    #     return STP
    # elif (EXP=='PAN'):
    #     PAN = ([0], )
    #     return PAN


# def landPopSelector(REL, PT_ROT):
#     if (REL=='265') or (REL=='265P'):
#         PT_UAS = path.join(
#             ''.join(PT_ROT.split('/'+REL)).replace('/sim/', ''),
#             'GEO', 'cluster_1', 'stp_cluster_sites_pop_v5_fixed.csv'
#         )
#     return (PT_UAS, path.join(PT_ROT, 'video'))



