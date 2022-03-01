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
        PT = aux.selectPathGeo(USR)
        if (EXP=='265_SP') or (EXP=='265_DP'):
            PAN = pkl.load(path.join(PT, 'clusters_002.bz'))
            return PAN
        elif (EXP=='265_SS') or (EXP=='265_DS'):
            SPA = pkl.load(path.join(PT, 'clusters_015.bz'))
            return SPA
        elif (EXP=='265_SF') or (EXP=='265_DF'):
            SPA = pkl.load(path.join(PT, 'clusters_075.bz'))
            return SPA
        elif (EXP=='265_SR') or (EXP=='265_DR'):
            SPA = pkl.load(path.join(PT, 'clusters_0{}.bz'.format(EXP[-2:])))
            return SPA



def landPopSelector(REL, PT_ROT):
    if (
        (REL=='265_SP') or (REL=='265_DP') or (REL=='265_SS') or 
        (REL=='265_DS') or (EXP=='265_SF') or (EXP=='265_DF') or
        (EXP=='265_SR') or (EXP=='265_DR')
    ):
        PT_UAS = path.join(
            ''.join(PT_ROT.split('/'+REL)).replace('/sim/', ''),
            'GEO', 'cluster_1', 'stp_cluster_sites_pop_v5_fixed.csv'
        )
    return (PT_UAS, path.join(PT_ROT, 'video'))


def landRelSelector(LND):
    if LND=='PAN':
        relStart = 5
    else:
        relStart = 100
    return relStart
