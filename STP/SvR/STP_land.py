#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import compress_pickle as pkl

def landSelector(land, REL, PT_ROT):
    if land == 'SPA':
        if REL == '265':
            pth = ''.join(PT_ROT.split('/'+REL)).replace('/sim/', '')
            STP = pkl.load(pth+ '/GEO/cluster_1/clusters.bz')
        elif REL == '505':
            pth = ''.join(PT_ROT.split('/'+REL)).replace('/sim/', '')
            STP = pkl.load(pth+ '/GEO/regular/clusters.bz')
        elif REL == '106':
            pth = ''.join(PT_ROT.split('/'+REL)).replace('/sim/', '')
            STP = pkl.load(pth+ '/GEO/cluster_2/clusters.bz')
        return STP
    else:
        PAN = ([0], )
        return PAN


def landPopSelector(REL, PT_ROT):
    if REL == '265':
        PT_UAS = path.join(
            ''.join(PT_ROT.split('/'+REL)).replace('/sim/', ''),
            'GEO', 'cluster_1', 'stp_cluster_sites_pop_v5_fixed.csv'
        )
    elif REL == '505':
        PT_UAS = path.join(
            ''.join(PT_ROT.split('/'+REL)).replace('/sim/', ''), 
            'GEO', 'regular', 'stp_all_sites_pop_v5_fixed.csv'
        )
    elif REL == '106':
        PT_UAS = path.join(
            ''.join(PT_ROT.split('/'+REL)).replace('/sim/', ''), 
            'GEO', 'cluster_2', 'stp_cluster_sites_pop_01_v5_fixed.csv'
        )
    return (PT_UAS, path.join(PT_ROT, 'video'))